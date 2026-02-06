#!/usr/bin/env python3
"""
Django QuerySet Optimization Checker
=====================================

Static analysis tool to detect N+1 query patterns and missing optimizations
in Django ViewSets and views.

Usage:
    python check_queryset_optimization.py <file_or_directory>
    python check_queryset_optimization.py views.py
    python check_queryset_optimization.py --check-all ./myapp/

Exit codes:
    0: No issues found
    1: Potential N+1 queries detected
    2: Script error

Author: Django Expert Skill
License: MIT
"""

import ast
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass


@dataclass
class Issue:
    """Represents a potential optimization issue."""
    file: str
    line: int
    severity: str  # 'critical', 'warning', 'info'
    message: str
    code_snippet: str


class QuerysetOptimizationChecker(ast.NodeVisitor):
    """AST visitor to detect N+1 query patterns."""
    
    def __init__(self, filepath: str, source_lines: List[str]):
        self.filepath = filepath
        self.source_lines = source_lines
        self.issues: List[Issue] = []
        self.current_class = None
        self.current_method = None
        self.has_select_related = False
        self.has_prefetch_related = False
        
    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Track current class context."""
        old_class = self.current_class
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = old_class
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Check methods for optimization patterns."""
        old_method = self.current_method
        self.current_method = node.name
        
        # Reset optimization flags for each method
        self.has_select_related = False
        self.has_prefetch_related = False
        
        # Check if this is a get_queryset method
        if node.name == 'get_queryset':
            self._check_get_queryset(node)
        
        # Check for N+1 in loops
        for child_node in ast.walk(node):
            if isinstance(child_node, (ast.For, ast.While)):
                self._check_loop_for_n_plus_one(child_node)
        
        self.generic_visit(node)
        self.current_method = old_method
    
    def visit_Attribute(self, node: ast.Attribute) -> None:
        """Track select_related and prefetch_related calls."""
        if node.attr == 'select_related':
            self.has_select_related = True
        elif node.attr == 'prefetch_related':
            self.has_prefetch_related = True
        self.generic_visit(node)
    
    def _check_get_queryset(self, node: ast.FunctionDef) -> None:
        """
        Check get_queryset method for optimization patterns.
        
        CRITICAL CHECKS:
        1. Must have select_related or prefetch_related
        2. Should handle different actions (list vs retrieve)
        """
        has_action_check = False
        has_optimization = False
        
        for child in ast.walk(node):
            # Check for self.action conditional
            if isinstance(child, ast.If):
                if self._checks_action(child.test):
                    has_action_check = True
            
            # Check for optimization calls
            if isinstance(child, ast.Attribute):
                if child.attr in ('select_related', 'prefetch_related'):
                    has_optimization = True
        
        # Issue: get_queryset without optimization
        if not has_optimization:
            self.issues.append(Issue(
                file=self.filepath,
                line=node.lineno,
                severity='critical',
                message=(
                    f"{self.current_class}.get_queryset() lacks "
                    "select_related/prefetch_related optimization"
                ),
                code_snippet=self._get_snippet(node.lineno, 3)
            ))
        
        # Warning: get_queryset without action-based optimization
        if has_optimization and not has_action_check:
            self.issues.append(Issue(
                file=self.filepath,
                line=node.lineno,
                severity='warning',
                message=(
                    f"{self.current_class}.get_queryset() should optimize "
                    "differently for 'list' vs 'retrieve' actions"
                ),
                code_snippet=self._get_snippet(node.lineno, 3)
            ))
    
    def _check_loop_for_n_plus_one(self, node: ast.For | ast.While) -> None:
        """
        Check for potential N+1 queries inside loops.
        
        Pattern detected:
            for item in queryset:
                related = item.foreign_key  # N+1!
                related_set = item.manytomany_set.all()  # N+1!
        """
        for child in ast.walk(node):
            # Detect attribute access that looks like FK/M2M access
            if isinstance(child, ast.Attribute):
                # Pattern: item.something (potential FK access)
                if isinstance(child.value, ast.Name):
                    # Check if accessing a relationship-like attribute
                    attr_name = child.attr
                    if self._looks_like_relationship(attr_name):
                        self.issues.append(Issue(
                            file=self.filepath,
                            line=child.lineno,
                            severity='critical',
                            message=(
                                f"Potential N+1 query: accessing '{attr_name}' "
                                f"inside loop in {self.current_class}.{self.current_method}(). "
                                f"Use select_related/prefetch_related."
                            ),
                            code_snippet=self._get_snippet(child.lineno, 2)
                        ))
    
    def _checks_action(self, node: ast.AST) -> bool:
        """Check if a condition tests self.action."""
        if isinstance(node, ast.Compare):
            if isinstance(node.left, ast.Attribute):
                if (isinstance(node.left.value, ast.Name) and 
                    node.left.value.id == 'self' and 
                    node.left.attr == 'action'):
                    return True
        return False
    
    def _looks_like_relationship(self, attr_name: str) -> bool:
        """
        Heuristic: check if attribute name looks like a relationship.
        
        Common patterns:
        - Ends with '_set' (reverse FK/M2M)
        - Contains 'related', 'foreign', 'parent', etc.
        - Common relationship names: user, project, deployment, etc.
        """
        relationship_patterns = [
            '_set',  # Django reverse relation
            'related',
            'parent',
            'child',
            'owner',
            'project',
            'deployment',
            'package',
            'computer',
            'attribute',
        ]
        
        attr_lower = attr_name.lower()
        return any(pattern in attr_lower for pattern in relationship_patterns)
    
    def _get_snippet(self, line: int, context_lines: int = 2) -> str:
        """Extract code snippet around the given line."""
        start = max(0, line - context_lines - 1)
        end = min(len(self.source_lines), line + context_lines)
        snippet_lines = self.source_lines[start:end]
        
        # Add line numbers
        numbered = [
            f"{start + i + 1:4d} | {line}"
            for i, line in enumerate(snippet_lines)
        ]
        return '\n'.join(numbered)


def check_file(filepath: Path) -> List[Issue]:
    """Check a single Python file for optimization issues."""
    try:
        source = filepath.read_text(encoding='utf-8')
        source_lines = source.splitlines()
        tree = ast.parse(source, filename=str(filepath))
        
        checker = QuerysetOptimizationChecker(str(filepath), source_lines)
        checker.visit(tree)
        
        return checker.issues
    except SyntaxError as e:
        return [Issue(
            file=str(filepath),
            line=e.lineno or 0,
            severity='error',
            message=f"Syntax error: {e.msg}",
            code_snippet=''
        )]
    except Exception as e:
        return [Issue(
            file=str(filepath),
            line=0,
            severity='error',
            message=f"Error processing file: {e}",
            code_snippet=''
        )]


def check_directory(dirpath: Path) -> List[Issue]:
    """Recursively check all Python files in a directory."""
    all_issues = []
    for pyfile in dirpath.rglob('*.py'):
        # Skip migrations
        if 'migrations' in pyfile.parts:
            continue
        all_issues.extend(check_file(pyfile))
    return all_issues


def format_issue(issue: Issue) -> str:
    """Format an issue for display."""
    severity_emoji = {
        'critical': '🔴',
        'warning': '🟡',
        'info': '🔵',
        'error': '💥',
    }
    
    emoji = severity_emoji.get(issue.severity, '⚠️')
    output = [
        f"\n{emoji} [{issue.severity.upper()}] {issue.file}:{issue.line}",
        f"   {issue.message}",
    ]
    
    if issue.code_snippet:
        output.append("\n   Code:")
        for line in issue.code_snippet.split('\n'):
            output.append(f"   {line}")
    
    return '\n'.join(output)


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Check Django code for QuerySet optimization issues'
    )
    parser.add_argument(
        'path',
        type=Path,
        help='File or directory to check'
    )
    parser.add_argument(
        '--check-all',
        action='store_true',
        help='Check all Python files recursively'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON'
    )
    
    args = parser.parse_args()
    
    # Collect issues
    if args.path.is_file():
        issues = check_file(args.path)
    elif args.path.is_dir():
        issues = check_directory(args.path)
    else:
        print(f"Error: {args.path} is not a valid file or directory", file=sys.stderr)
        return 2
    
    # Output results
    if args.json:
        import json
        print(json.dumps([
            {
                'file': issue.file,
                'line': issue.line,
                'severity': issue.severity,
                'message': issue.message,
            }
            for issue in issues
        ], indent=2))
    else:
        if not issues:
            print("✅ No optimization issues found!")
            return 0
        
        print(f"\n{'='*80}")
        print(f"Found {len(issues)} potential optimization issue(s)")
        print(f"{'='*80}")
        
        for issue in issues:
            print(format_issue(issue))
        
        print(f"\n{'='*80}")
        
        # Summary by severity
        from collections import Counter
        severity_counts = Counter(issue.severity for issue in issues)
        print("\nSummary:")
        for severity in ['critical', 'warning', 'info', 'error']:
            count = severity_counts.get(severity, 0)
            if count > 0:
                print(f"  {severity.capitalize()}: {count}")
    
    # Exit code based on critical issues
    has_critical = any(issue.severity == 'critical' for issue in issues)
    return 1 if has_critical else 0


if __name__ == '__main__':
    sys.exit(main())

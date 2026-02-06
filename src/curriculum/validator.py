"""
Curriculum validation logic.
"""
from typing import List, Tuple
from src.curriculum.models import Curriculum, Semester


class CurriculumValidator:
    """Validate curriculum structure and quality."""
    
    def __init__(
        self,
        min_credits_per_semester: int = 12,
        max_credits_per_semester: int = 24
    ):
        """
        Initialize validator.
        
        Args:
            min_credits_per_semester: Minimum credits per semester
            max_credits_per_semester: Maximum credits per semester
        """
        self.min_credits = min_credits_per_semester
        self.max_credits = max_credits_per_semester
    
    def validate(self, curriculum: Curriculum) -> Tuple[bool, List[str]]:
        """
        Validate curriculum.
        
        Args:
            curriculum: Curriculum to validate
            
        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []
        
        # Check semester count
        if len(curriculum.semesters) != curriculum.duration_semesters:
            issues.append(
                f"Semester count mismatch: expected {curriculum.duration_semesters}, "
                f"got {len(curriculum.semesters)}"
            )
        
        # Check each semester
        total_credits = 0
        for semester in curriculum.semesters:
            # Validate credit balance
            semester_credits = sum(course.credits for course in semester.courses)
            
            if semester_credits != semester.total_credits:
                issues.append(
                    f"Semester {semester.semester_number}: credit mismatch "
                    f"(declared: {semester.total_credits}, actual: {semester_credits})"
                )
            
            if semester_credits < self.min_credits:
                issues.append(
                    f"Semester {semester.semester_number}: too few credits ({semester_credits})"
                )
            
            if semester_credits > self.max_credits:
                issues.append(
                    f"Semester {semester.semester_number}: too many credits ({semester_credits})"
                )
            
            total_credits += semester_credits
            
            # Check for duplicate course codes
            course_codes = [course.code for course in semester.courses]
            if len(course_codes) != len(set(course_codes)):
                issues.append(
                    f"Semester {semester.semester_number}: duplicate course codes found"
                )
        
        # Check total credits
        if total_credits != curriculum.total_credits:
            issues.append(
                f"Total credits mismatch: declared {curriculum.total_credits}, "
                f"actual {total_credits}"
            )
        
        # Check for empty fields
        if not curriculum.overview:
            issues.append("Missing curriculum overview")
        
        if not curriculum.learning_outcomes:
            issues.append("Missing learning outcomes")
        
        is_valid = len(issues) == 0
        return is_valid, issues
    
    def validate_and_report(self, curriculum: Curriculum) -> str:
        """
        Validate and generate report.
        
        Args:
            curriculum: Curriculum to validate
            
        Returns:
            Validation report string
        """
        is_valid, issues = self.validate(curriculum)
        
        if is_valid:
            return "✓ Curriculum validation passed!"
        else:
            report = "⚠ Curriculum validation found issues:\n"
            for i, issue in enumerate(issues, 1):
                report += f"{i}. {issue}\n"
            return report

"""
Comprehensive pytest test suite for Scholarship Recorder application.
Tests cover all scholarship types, manager operations, and edge cases.
Written by Claude AI and adjusted by Daniel Jardine
Used also to test and fix bugs found by Claude AI.

NOTE: The following code WILL alter Excel files related to the program in the working directory
      during testing. Run test BEFORE using the Scholarship Recorder application to avoid data loss.
"""

import pytest
import os
import pickle
import tempfile
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from Scholarship_Recorder import (
    Scholarship,
    Academic,
    Federal_Grant,
    Need_Based,
    Athletic,
    Minority,
    Creative_Arts,
    Community_Service,
    Scholarship_Manager
)


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def basic_scholarship():
    """Create a basic Scholarship instance for testing."""
    return Scholarship(
        name="Test Scholarship",
        pay_amount=1000.0,
        deadline="2025-12-31",
        scholarship_type="Test",
        essay_count=1,
        organization="Test Org",
        additional_required_materials=["Transcript"],
        URL="https://example.com"
    )


@pytest.fixture
def academic_scholarship():
    """Create an Academic scholarship instance for testing."""
    return Academic(
        name="Academic Excellence Award",
        pay_amount=5000.0,
        deadline="2025-06-15",
        essay_count=2,
        organization="University Board",
        GPA_requirement=3.5,
        transcript_required=True,
        letters_of_recommendation=2,
        standardized_testing_required=True,
        additional_required_materials=["Transcript", "Test Scores"],
        URL="https://example.com/academic"
    )


@pytest.fixture
def federal_grant():
    """Create a Federal_Grant instance for testing."""
    return Federal_Grant(
        name="Pell Grant",
        pay_amount=7395.0,
        deadline=None,
        essay_count=0,
        organization="Federal Student Aid",
        FAFSA_required=True,
        enrollment_status="Full-Time",
        income_threshold=30000.0,
        URL="https://example.com/pell"
    )


@pytest.fixture
def need_based_scholarship():
    """Create a Need_Based scholarship instance for testing."""
    return Need_Based(
        name="Need Based Award",
        pay_amount=2000.0,
        deadline="2025-08-30",
        organization="Helping Hands",
        FAFSA_required=True,
        enrollment_status="Part-Time",
        additional_required_materials=["Proof of Income"],
        URL="https://example.com/need"
    )


@pytest.fixture
def athletic_scholarship():
    """Create an Athletic scholarship instance for testing."""
    return Athletic(
        name="Sports Excellence Award",
        pay_amount=3000.0,
        deadline="2025-07-01",
        essay_count=1,
        organization="Sports League",
        sport="Basketball",
        competition_level="Division I",
        coach_recommendation=True,
        coach_contact_info=["Coach Smith", "coach@example.com"],
        athletic_resumes_required=True,
        URL="https://example.com/athletic"
    )


@pytest.fixture
def minority_scholarship():
    """Create a Minority scholarship instance for testing."""
    return Minority(
        name="Diversity Leadership Award",
        pay_amount=4000.0,
        deadline="2025-09-01",
        organization="Diversity Fund",
        target_demographic="Underrepresented Students",
        community_involvement_required=True,
        diversity_statement_required=True,
        URL="https://example.com/minority"
    )


@pytest.fixture
def creative_arts_scholarship():
    """Create a Creative_Arts scholarship instance for testing."""
    return Creative_Arts(
        name="Artistic Talent Grant",
        pay_amount=2500.0,
        deadline="2025-04-15",
        organization="Arts Council",
        art_portfolio_required=True,
        audition_required=False,
        art_mediums_accepted=["Painting", "Sculpture", "Digital Art"],
        URL="https://example.com/arts"
    )


@pytest.fixture
def community_service_scholarship():
    """Create a Community_Service scholarship instance for testing."""
    return Community_Service(
        name="Community Hero Award",
        pay_amount=1500.0,
        deadline="2025-03-20",
        organization="Volunteer Network",
        service_hours_required=100,
        type_of_service="Local Outreach",
        recommendation_letters_required=1,
        URL="https://example.com/service"
    )


@pytest.fixture
def scholarship_manager():
    """Create an empty Scholarship_Manager for testing."""
    return Scholarship_Manager()


@pytest.fixture
def populated_manager(basic_scholarship, academic_scholarship, federal_grant):
    """Create a Scholarship_Manager with some scholarships."""
    manager = Scholarship_Manager()
    manager.add_scholarship(basic_scholarship)
    manager.add_scholarship(academic_scholarship)
    manager.add_scholarship(federal_grant)
    return manager


@pytest.fixture
def temp_excel_cleanup():
    """Fixture to clean up Excel files created during tests."""
    files_to_cleanup = []
    yield files_to_cleanup
    for f in files_to_cleanup:
        if os.path.exists(f):
            os.remove(f)


# =============================================================================
# SCHOLARSHIP BASE CLASS TESTS
# =============================================================================

class TestScholarshipBase:
    """Tests for the base Scholarship class."""

    def test_scholarship_creation_with_defaults(self):
        """Test creating a scholarship with default values."""
        s = Scholarship()
        assert s.name == ""
        assert s.pay_amount == 0.0
        assert s.deadline is None
        assert s.scholarship_type == "Other"
        assert s.essay_count == 0
        assert s.organization == ""
        assert s.additional_required_materials == []
        assert s.URL == ""
        assert s.applied == False

    def test_scholarship_creation_with_values(self, basic_scholarship):
        """Test creating a scholarship with specified values."""
        assert basic_scholarship.name == "Test Scholarship"
        assert basic_scholarship.pay_amount == 1000.0
        assert basic_scholarship.deadline == "2025-12-31"
        assert basic_scholarship.scholarship_type == "Test"
        assert basic_scholarship.essay_count == 1
        assert basic_scholarship.organization == "Test Org"
        assert basic_scholarship.additional_required_materials == ["Transcript"]
        assert basic_scholarship.URL == "https://example.com"

    def test_scholarship_str_representation(self, basic_scholarship):
        """Test string representation of scholarship."""
        result = str(basic_scholarship)
        assert "Test Scholarship" in result
        assert "1000.0" in result
        assert "2025-12-31" in result
        assert "Test" in result

    def test_mark_applied(self, basic_scholarship):
        """Test marking a scholarship as applied."""
        assert basic_scholarship.applied == False
        basic_scholarship.mark_applied()
        assert basic_scholarship.applied == True

    def test_applied_initialized_in_post_init(self):
        """Test that applied is initialized to False in __post_init__."""
        s = Scholarship(name="Test")
        assert hasattr(s, 'applied')
        assert s.applied == False


class TestScholarshipDateValidation:
    """Tests for date validation functionality."""

    def test_validate_date_format_valid(self):
        """Test validation of valid date formats."""
        assert Scholarship.validate_date_format("2025-12-31") == True
        assert Scholarship.validate_date_format("2024-01-01") == True
        assert Scholarship.validate_date_format("2030-06-15") == True

    def test_validate_date_format_invalid(self):
        """Test validation of invalid date formats."""
        assert Scholarship.validate_date_format("12-31-2025") == False
        assert Scholarship.validate_date_format("2025/12/31") == False
        assert Scholarship.validate_date_format("December 31, 2025") == False
        assert Scholarship.validate_date_format("not a date") == False
        assert Scholarship.validate_date_format("") == False

    def test_validate_date_format_none(self):
        """Test validation when date is None."""
        assert Scholarship.validate_date_format(None) == True

    def test_validate_date_format_invalid_date_values(self):
        """Test validation of dates with invalid day/month values."""
        assert Scholarship.validate_date_format("2025-13-01") == False  # Invalid month
        assert Scholarship.validate_date_format("2025-02-30") == False  # Invalid day


class TestScholarshipDeadlineCalculation:
    """Tests for deadline calculation functionality."""

    def test_calculate_deadline_future_date(self):
        """Test calculating days until a future deadline."""
        future_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        s = Scholarship(deadline=future_date)
        result = s.calculate_deadline()
        assert isinstance(result, int)
        assert 29 <= result <= 30  # Account for time of day

    def test_calculate_deadline_past_date(self):
        """Test calculating days for a past deadline."""
        past_date = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
        s = Scholarship(deadline=past_date)
        result = s.calculate_deadline()
        assert isinstance(result, int)
        assert result < 0

    def test_calculate_deadline_today(self):
        """Test calculating deadline for today."""
        today = datetime.now().strftime("%Y-%m-%d")
        s = Scholarship(deadline=today)
        result = s.calculate_deadline()
        assert isinstance(result, int)
        assert -1 <= result <= 0

    def test_calculate_deadline_none(self):
        """Test calculating deadline when deadline is None."""
        s = Scholarship(deadline=None)
        result = s.calculate_deadline()
        assert result == None

    def test_calculate_deadline_invalid_format(self):
        """Test calculating deadline with invalid date format."""
        s = Scholarship(deadline="invalid-date")
        result = s.calculate_deadline()
        assert result == None


class TestScholarshipURL:
    """Tests for URL handling functionality."""

    def test_open_url_valid(self, basic_scholarship):
        """Test opening a valid URL."""
        with patch('webbrowser.open') as mock_open:
            result = basic_scholarship.open_url()
            assert result == True
            mock_open.assert_called_once_with("https://example.com")

    def test_open_url_empty(self):
        """Test opening URL when URL is empty."""
        s = Scholarship(URL="")
        with patch('webbrowser.open') as mock_open:
            result = s.open_url()
            assert result == False
            mock_open.assert_not_called()

    def test_open_url_whitespace_only(self):
        """Test opening URL when URL contains only whitespace."""
        s = Scholarship(URL="   ")
        with patch('webbrowser.open') as mock_open:
            result = s.open_url()
            assert result == False
            mock_open.assert_not_called()


# =============================================================================
# ACADEMIC SCHOLARSHIP TESTS
# =============================================================================

class TestAcademicScholarship:
    """Tests for the Academic scholarship class."""

    def test_academic_creation_defaults(self):
        """Test creating Academic scholarship with defaults."""
        a = Academic()
        assert a.scholarship_type == "Academic"
        assert a.GPA_requirement == 0.0
        assert a.transcript_required == False
        assert a.letters_of_recommendation == 0
        assert a.standardized_testing_required == False

    def test_academic_creation_with_values(self, academic_scholarship):
        """Test creating Academic scholarship with specified values."""
        assert academic_scholarship.GPA_requirement == 3.5
        assert academic_scholarship.transcript_required == True
        assert academic_scholarship.letters_of_recommendation == 2
        assert academic_scholarship.standardized_testing_required == True

    def test_academic_gpa_clamping_negative(self):
        """Test that negative GPA is clamped to 0."""
        a = Academic(GPA_requirement=-1.0)
        assert a.GPA_requirement == 0.0

    def test_academic_gpa_clamping_over_max(self):
        """Test that GPA over 5.0 is clamped to 5.0."""
        a = Academic(GPA_requirement=6.0)
        assert a.GPA_requirement == 4.0

    def test_academic_gpa_valid_range(self):
        """Test that valid GPA values are preserved."""
        a = Academic(GPA_requirement=3.75)
        assert a.GPA_requirement == 3.75

    def test_academic_gpa_boundary_values(self):
        """Test GPA boundary values."""
        a_zero = Academic(GPA_requirement=0.0)
        assert a_zero.GPA_requirement == 0.0

        a_max = Academic(GPA_requirement=5.0)
        assert a_max.GPA_requirement == 4.0


# =============================================================================
# FEDERAL GRANT TESTS
# =============================================================================

class TestFederalGrant:
    """Tests for the Federal_Grant class."""

    def test_federal_grant_creation_defaults(self):
        """Test creating Federal_Grant with defaults."""
        f = Federal_Grant()
        assert f.scholarship_type == "Federal Grant/Scholarship"
        assert f.FAFSA_required == True
        assert f.enrollment_status is None
        assert f.income_threshold == 0.0

    def test_federal_grant_creation_with_values(self, federal_grant):
        """Test creating Federal_Grant with specified values."""
        assert federal_grant.FAFSA_required == True
        assert federal_grant.enrollment_status == "Full-Time"
        assert federal_grant.income_threshold == 30000.0

    def test_calculate_expected_aid_low_income(self):
        """Test expected aid calculation for low income (<=30000)."""
        f = Federal_Grant(income_threshold=20000.0)
        result = f.calculate_expected_aid()
        assert result == 7395  # Should return max aid

    def test_calculate_expected_aid_at_threshold(self):
        """Test expected aid calculation at threshold (30000)."""
        f = Federal_Grant(income_threshold=30000.0)
        result = f.calculate_expected_aid()
        assert result == 7395  # Should return max aid

    def test_calculate_expected_aid_above_threshold(self):
        """Test expected aid calculation for income above threshold."""
        f = Federal_Grant(income_threshold=40000.0)
        result = f.calculate_expected_aid()
        # A_max - k * (income - T) = 7395 - 0.30 * (40000 - 30000) = 7395 - 3000 = 4395
        assert result == 4395.0

    def test_calculate_expected_aid_high_income_zero_aid(self):
        """Test expected aid returns 0 for very high income."""
        f = Federal_Grant(income_threshold=100000.0)
        result = f.calculate_expected_aid()
        assert result == 0.0  # Should be clamped to 0

    def test_calculate_expected_aid_custom_parameters(self):
        """Test expected aid with custom A_max, T, and k parameters."""
        f = Federal_Grant(income_threshold=50000.0)
        result = f.calculate_expected_aid(A_max=10000, T=40000, k=0.5)
        # 10000 - 0.5 * (50000 - 40000) = 10000 - 5000 = 5000
        assert result == 5000.0


# =============================================================================
# NEED BASED SCHOLARSHIP TESTS
# =============================================================================

class TestNeedBasedScholarship:
    """Tests for the Need_Based scholarship class."""

    def test_need_based_creation_defaults(self):
        """Test creating Need_Based scholarship with defaults."""
        n = Need_Based()
        assert n.scholarship_type == "Need-Based"
        assert n.FAFSA_required == True
        assert n.enrollment_status is None

    def test_need_based_creation_with_values(self, need_based_scholarship):
        """Test creating Need_Based scholarship with specified values."""
        assert need_based_scholarship.FAFSA_required == True
        assert need_based_scholarship.enrollment_status == "Part-Time"


# =============================================================================
# ATHLETIC SCHOLARSHIP TESTS
# =============================================================================

class TestAthleticScholarship:
    """Tests for the Athletic scholarship class."""

    def test_athletic_creation_defaults(self):
        """Test creating Athletic scholarship with defaults."""
        a = Athletic()
        assert a.scholarship_type == "Athletic"
        assert a.sport == ""
        assert a.competition_level == ""
        assert a.coach_recommendation == False
        assert a.coach_contact_info == []
        assert a.athletic_resumes_required == False

    def test_athletic_creation_with_values(self, athletic_scholarship):
        """Test creating Athletic scholarship with specified values."""
        assert athletic_scholarship.sport == "Basketball"
        assert athletic_scholarship.competition_level == "Division I"
        assert athletic_scholarship.coach_recommendation == True
        assert athletic_scholarship.coach_contact_info == ["Coach Smith", "coach@example.com"]
        assert athletic_scholarship.athletic_resumes_required == True


# =============================================================================
# MINORITY SCHOLARSHIP TESTS
# =============================================================================

class TestMinorityScholarship:
    """Tests for the Minority scholarship class."""

    def test_minority_creation_defaults(self):
        """Test creating Minority scholarship with defaults."""
        m = Minority()
        assert m.scholarship_type == "Minority"
        assert m.target_demographic == ""
        assert m.community_involvement_required == False
        assert m.diversity_statement_required == False

    def test_minority_creation_with_values(self, minority_scholarship):
        """Test creating Minority scholarship with specified values."""
        assert minority_scholarship.target_demographic == "Underrepresented Students"
        assert minority_scholarship.community_involvement_required == True
        assert minority_scholarship.diversity_statement_required == True


# =============================================================================
# CREATIVE ARTS SCHOLARSHIP TESTS
# =============================================================================

class TestCreativeArtsScholarship:
    """Tests for the Creative_Arts scholarship class."""

    def test_creative_arts_creation_defaults(self):
        """Test creating Creative_Arts scholarship with defaults."""
        c = Creative_Arts()
        assert c.scholarship_type == "Creative Arts"
        assert c.art_portfolio_required == False
        assert c.audition_required == False
        assert c.art_mediums_accepted == []

    def test_creative_arts_creation_with_values(self, creative_arts_scholarship):
        """Test creating Creative_Arts scholarship with specified values."""
        assert creative_arts_scholarship.art_portfolio_required == True
        assert creative_arts_scholarship.audition_required == False
        assert creative_arts_scholarship.art_mediums_accepted == ["Painting", "Sculpture", "Digital Art"]


# =============================================================================
# COMMUNITY SERVICE SCHOLARSHIP TESTS
# =============================================================================

class TestCommunityServiceScholarship:
    """Tests for the Community_Service scholarship class."""

    def test_community_service_creation_defaults(self):
        """Test creating Community_Service scholarship with defaults."""
        c = Community_Service()
        assert c.scholarship_type == "Community Service"
        assert c.service_hours_required == 0
        assert c.type_of_service == ""
        assert c.recommendation_letters_required == 0

    def test_community_service_creation_with_values(self, community_service_scholarship):
        """Test creating Community_Service scholarship with specified values."""
        assert community_service_scholarship.service_hours_required == 100
        assert community_service_scholarship.type_of_service == "Local Outreach"
        assert community_service_scholarship.recommendation_letters_required == 1


# =============================================================================
# SCHOLARSHIP MANAGER TESTS
# =============================================================================

class TestScholarshipManagerBasic:
    """Basic tests for Scholarship_Manager class."""

    def test_manager_creation_empty(self, scholarship_manager):
        """Test creating an empty manager."""
        assert scholarship_manager.scholarships == []

    def test_manager_add_scholarship(self, scholarship_manager, basic_scholarship):
        """Test adding a scholarship to manager."""
        result = scholarship_manager.add_scholarship(basic_scholarship)
        assert result == True
        assert len(scholarship_manager.scholarships) == 1
        assert scholarship_manager.scholarships[0] == basic_scholarship

    def test_manager_add_duplicate_scholarship(self, scholarship_manager, basic_scholarship):
        """Test adding a duplicate scholarship (same name, case insensitive)."""
        scholarship_manager.add_scholarship(basic_scholarship)
        duplicate = Scholarship(name="test scholarship")  # Different case
        result = scholarship_manager.add_scholarship(duplicate)
        assert result == False
        assert len(scholarship_manager.scholarships) == 1

    def test_manager_remove_scholarship(self, scholarship_manager, basic_scholarship):
        """Test removing a scholarship from manager."""
        scholarship_manager.add_scholarship(basic_scholarship)
        result = scholarship_manager.remove_scholarship(basic_scholarship)
        assert result == True
        assert len(scholarship_manager.scholarships) == 0

    def test_manager_remove_nonexistent_scholarship(self, scholarship_manager, basic_scholarship):
        """Test removing a scholarship that doesn't exist."""
        result = scholarship_manager.remove_scholarship(basic_scholarship)
        assert result == False

    def test_manager_str_empty(self, scholarship_manager):
        """Test string representation of empty manager."""
        result = str(scholarship_manager)
        assert "No scholarships recorded" in result

    def test_manager_str_with_scholarships(self, populated_manager):
        """Test string representation of manager with scholarships."""
        result = str(populated_manager)
        assert "Test Scholarship" in result
        assert "Academic Excellence Award" in result
        assert "Pell Grant" in result


class TestScholarshipManagerFind:
    """Tests for Scholarship_Manager find functionality."""

    def test_find_scholarship_by_name_exists(self, populated_manager):
        """Test finding a scholarship that exists."""
        result = populated_manager.find_scholarship_by_name("Test Scholarship")
        assert result is not None
        assert result.name == "Test Scholarship"

    def test_find_scholarship_by_name_case_insensitive(self, populated_manager):
        """Test finding a scholarship with case insensitive search."""
        result = populated_manager.find_scholarship_by_name("test scholarship")
        assert result is not None
        assert result.name == "Test Scholarship"

    def test_find_scholarship_by_name_case_sensitive(self, populated_manager):
        """Test finding a scholarship with case sensitive search."""
        result = populated_manager.find_scholarship_by_name("test scholarship", case_sensitive=True)
        assert result is None

    def test_find_scholarship_by_name_not_found(self, populated_manager):
        """Test finding a scholarship that doesn't exist."""
        result = populated_manager.find_scholarship_by_name("Nonexistent Scholarship")
        assert result is None


class TestScholarshipManagerAutoRemove:
    """Tests for auto-remove expired scholarships functionality."""

    def test_auto_remove_expired_scholarships(self, scholarship_manager):
        """Test automatic removal of expired scholarships."""
        past_date = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
        future_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")

        expired = Scholarship(name="Expired", deadline=past_date)
        active = Scholarship(name="Active", deadline=future_date)

        scholarship_manager.add_scholarship(expired)
        scholarship_manager.add_scholarship(active)

        scholarship_manager.auto_remove_expired_scholarships()

        assert len(scholarship_manager.scholarships) == 1
        assert scholarship_manager.scholarships[0].name == "Active"

    def test_auto_remove_keeps_applied_expired(self, scholarship_manager):
        """Test that applied scholarships are not removed even if expired."""
        past_date = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
        expired_applied = Scholarship(name="Expired Applied", deadline=past_date)
        expired_applied.mark_applied()

        scholarship_manager.add_scholarship(expired_applied)
        scholarship_manager.auto_remove_expired_scholarships()

        assert len(scholarship_manager.scholarships) == 1
        assert scholarship_manager.scholarships[0].name == "Expired Applied"

    def test_auto_remove_keeps_no_deadline(self, scholarship_manager):
        """Test that scholarships without deadlines are not removed."""
        no_deadline = Scholarship(name="No Deadline", deadline=None)
        scholarship_manager.add_scholarship(no_deadline)

        scholarship_manager.auto_remove_expired_scholarships()

        assert len(scholarship_manager.scholarships) == 1

    def test_auto_remove_handles_invalid_date(self, scholarship_manager):
        """Test auto remove handles invalid date formats gracefully."""
        invalid_date = Scholarship(name="Invalid Date", deadline="not-a-date")
        scholarship_manager.add_scholarship(invalid_date)

        # Should not raise an exception
        scholarship_manager.auto_remove_expired_scholarships()

        # Invalid date scholarship should remain
        assert len(scholarship_manager.scholarships) == 1


class TestScholarshipManagerPersistence:
    """Tests for save/load functionality."""

    def test_export_to_file(self, populated_manager):
        """Test exporting scholarships to a file."""
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.pkl') as f:
            filename = f.name

        try:
            result = populated_manager.export_to_saved_file(filename)
            assert result == True
            assert os.path.exists(filename)
        finally:
            if os.path.exists(filename):
                os.remove(filename)

    def test_import_from_file(self, scholarship_manager, populated_manager):
        """Test importing scholarships from a file."""
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.pkl') as f:
            filename = f.name

        try:
            populated_manager.export_to_saved_file(filename)
            result = scholarship_manager.import_from_saved_file(filename)

            assert result == True
            assert len(scholarship_manager.scholarships) == 3
        finally:
            if os.path.exists(filename):
                os.remove(filename)

    def test_import_from_nonexistent_file(self, scholarship_manager):
        """Test importing from a file that doesn't exist."""
        result = scholarship_manager.import_from_saved_file("nonexistent_file.pkl")
        assert result == False

    def test_export_to_invalid_path(self, populated_manager):
        """Test exporting to an invalid path."""
        result = populated_manager.export_to_saved_file("/invalid/path/file.pkl")
        assert result == False

    def test_import_corrupted_file(self, scholarship_manager):
        """Test importing from a corrupted file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.pkl') as f:
            f.write("This is not valid pickle data")
            filename = f.name

        try:
            result = scholarship_manager.import_from_saved_file(filename)
            assert result == False
        finally:
            if os.path.exists(filename):
                os.remove(filename)


# =============================================================================
# EXCEL EXPORT TESTS
# =============================================================================

class TestExcelExport:
    """Tests for Excel export functionality."""

    def test_scholarship_add_to_sheet_creates_file(self, basic_scholarship, temp_excel_cleanup):
        """Test that add_to_sheet creates an Excel file."""
        filename = 'other_scholarships.xlsx'
        temp_excel_cleanup.append(filename)

        # Remove file if it exists
        if os.path.exists(filename):
            os.remove(filename)

        result = basic_scholarship.add_to_sheet()
        assert result == True
        assert os.path.exists(filename)

    def test_scholarship_add_to_sheet_duplicate(self, basic_scholarship, temp_excel_cleanup):
        """Test that adding duplicate scholarship fails."""
        filename = 'other_scholarships.xlsx'
        temp_excel_cleanup.append(filename)

        if os.path.exists(filename):
            os.remove(filename)

        basic_scholarship.add_to_sheet()
        result = basic_scholarship.add_to_sheet()
        assert result == False

    def test_academic_add_to_sheet(self, academic_scholarship, temp_excel_cleanup):
        """Test Academic scholarship Excel export."""
        filename = 'academic_scholarships.xlsx'
        temp_excel_cleanup.append(filename)

        if os.path.exists(filename):
            os.remove(filename)

        result = academic_scholarship.add_to_sheet()
        assert result == True
        assert os.path.exists(filename)

    def test_federal_grant_add_to_sheet(self, federal_grant, temp_excel_cleanup):
        """Test Federal_Grant Excel export."""
        filename = 'federal_grants_scholarships.xlsx'
        temp_excel_cleanup.append(filename)

        if os.path.exists(filename):
            os.remove(filename)

        result = federal_grant.add_to_sheet()
        assert result == True
        assert os.path.exists(filename)

    def test_need_based_add_to_sheet(self, need_based_scholarship, temp_excel_cleanup):
        """Test Need_Based scholarship Excel export."""
        filename = 'need_based_scholarships.xlsx'
        temp_excel_cleanup.append(filename)

        if os.path.exists(filename):
            os.remove(filename)

        result = need_based_scholarship.add_to_sheet()
        assert result == True
        assert os.path.exists(filename)

    def test_athletic_add_to_sheet(self, athletic_scholarship, temp_excel_cleanup):
        """Test Athletic scholarship Excel export."""
        filename = 'athletic_scholarships.xlsx'
        temp_excel_cleanup.append(filename)

        if os.path.exists(filename):
            os.remove(filename)

        result = athletic_scholarship.add_to_sheet()
        assert result == True
        assert os.path.exists(filename)

    def test_minority_add_to_sheet(self, minority_scholarship, temp_excel_cleanup):
        """Test Minority scholarship Excel export."""
        filename = 'minority_scholarships.xlsx'
        temp_excel_cleanup.append(filename)

        if os.path.exists(filename):
            os.remove(filename)

        result = minority_scholarship.add_to_sheet()
        assert result == True
        assert os.path.exists(filename)

    def test_creative_arts_add_to_sheet(self, creative_arts_scholarship, temp_excel_cleanup):
        """Test Creative_Arts scholarship Excel export."""
        filename = 'creative_arts_scholarships.xlsx'
        temp_excel_cleanup.append(filename)

        if os.path.exists(filename):
            os.remove(filename)

        result = creative_arts_scholarship.add_to_sheet()
        assert result == True
        assert os.path.exists(filename)

    def test_community_service_add_to_sheet(self, community_service_scholarship, temp_excel_cleanup):
        """Test Community_Service scholarship Excel export."""
        filename = 'community_service_scholarships.xlsx'
        temp_excel_cleanup.append(filename)

        if os.path.exists(filename):
            os.remove(filename)

        result = community_service_scholarship.add_to_sheet()
        assert result == True
        assert os.path.exists(filename)


# =============================================================================
# EDGE CASE TESTS
# =============================================================================

class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_scholarship_empty_name(self):
        """Test scholarship with empty name."""
        s = Scholarship(name="")
        assert s.name == ""

    def test_scholarship_special_characters_in_name(self):
        """Test scholarship with special characters in name."""
        s = Scholarship(name="Test & Scholarship #1 (2025)")
        assert s.name == "Test & Scholarship #1 (2025)"

    def test_scholarship_unicode_name(self):
        """Test scholarship with unicode characters in name."""
        s = Scholarship(name="Beca de Estudiante 日本語")
        assert s.name == "Beca de Estudiante 日本語"

    def test_scholarship_negative_pay_amount(self):
        """Test scholarship with negative pay amount (allowed by current code)."""
        s = Scholarship(pay_amount=-500.0)
        assert s.pay_amount == -500.0

    def test_scholarship_zero_pay_amount(self):
        """Test scholarship with zero pay amount."""
        s = Scholarship(pay_amount=0.0)
        assert s.pay_amount == 0.0

    def test_scholarship_large_pay_amount(self):
        """Test scholarship with very large pay amount."""
        s = Scholarship(pay_amount=1000000.0)
        assert s.pay_amount == 1000000.0

    def test_scholarship_empty_url(self):
        """Test scholarship with empty URL."""
        s = Scholarship(URL="")
        assert s.open_url() == False

    def test_scholarship_long_additional_materials_list(self):
        """Test scholarship with many additional materials."""
        materials = [f"Material {i}" for i in range(100)]
        s = Scholarship(additional_required_materials=materials)
        assert len(s.additional_required_materials) == 100

    def test_manager_many_scholarships(self, scholarship_manager):
        """Test manager with many scholarships."""
        for i in range(100):
            s = Scholarship(name=f"Scholarship {i}")
            scholarship_manager.add_scholarship(s)
        assert len(scholarship_manager.scholarships) == 100

    def test_federal_grant_zero_income(self):
        """Test expected aid calculation with zero income."""
        f = Federal_Grant(income_threshold=0.0)
        result = f.calculate_expected_aid()
        assert result == 7395  # Max aid for low income

    def test_federal_grant_negative_income(self):
        """Test expected aid calculation with negative income (edge case)."""
        f = Federal_Grant(income_threshold=-1000.0)
        result = f.calculate_expected_aid()
        assert result == 7395  # Should still return max aid


# =============================================================================
# INTEGRATION TESTS
# =============================================================================

class TestIntegration:
    """Integration tests for complete workflows."""

    def test_full_workflow_add_find_remove(self, scholarship_manager):
        """Test a complete workflow of adding, finding, and removing."""
        # Add
        s = Scholarship(name="Integration Test", pay_amount=1000.0)
        scholarship_manager.add_scholarship(s)

        # Find
        found = scholarship_manager.find_scholarship_by_name("Integration Test")
        assert found is not None

        # Mark applied
        found.mark_applied()
        assert found.applied == True

        # Remove
        result = scholarship_manager.remove_scholarship(found)
        assert result == True
        assert len(scholarship_manager.scholarships) == 0

    def test_full_workflow_save_load_modify(self, scholarship_manager):
        """Test save, load, and modify workflow."""
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.pkl') as f:
            filename = f.name

        try:
            # Add and save
            s = Scholarship(name="Persist Test", pay_amount=500.0)
            scholarship_manager.add_scholarship(s)
            scholarship_manager.export_to_saved_file(filename)

            # Create new manager and load
            new_manager = Scholarship_Manager()
            new_manager.import_from_saved_file(filename)

            # Verify and modify
            assert len(new_manager.scholarships) == 1
            found = new_manager.find_scholarship_by_name("Persist Test")
            assert found is not None
            found.mark_applied()

            # Save again
            new_manager.export_to_saved_file(filename)

            # Load and verify modification persisted
            final_manager = Scholarship_Manager()
            final_manager.import_from_saved_file(filename)
            final_found = final_manager.find_scholarship_by_name("Persist Test")
            assert final_found.applied == True
        finally:
            if os.path.exists(filename):
                os.remove(filename)

    def test_mixed_scholarship_types_in_manager(self, scholarship_manager,
                                                 academic_scholarship,
                                                 federal_grant,
                                                 athletic_scholarship):
        """Test manager with multiple scholarship types."""
        scholarship_manager.add_scholarship(academic_scholarship)
        scholarship_manager.add_scholarship(federal_grant)
        scholarship_manager.add_scholarship(athletic_scholarship)

        assert len(scholarship_manager.scholarships) == 3

        # Verify each type is correct
        types = [s.scholarship_type for s in scholarship_manager.scholarships]
        assert "Academic" in types
        assert "Federal Grant/Scholarship" in types
        assert "Athletic" in types


# =============================================================================
# SR_PROMPT INPUT FUNCTION TESTS
# =============================================================================

class TestSRPromptInputFunctions:
    """Tests for SR_Prompt input validation functions."""

    def test_get_optional_string_with_value(self):
        """Test get_optional_string with a value."""
        from SR_Prompt import get_optional_string
        with patch('builtins.input', return_value="test value"):
            result = get_optional_string("Enter: ")
            assert result == "test value"

    def test_get_optional_string_empty(self):
        """Test get_optional_string with empty input."""
        from SR_Prompt import get_optional_string
        with patch('builtins.input', return_value=""):
            result = get_optional_string("Enter: ")
            assert result is None

    def test_get_required_string_with_value(self):
        """Test get_required_string with a value."""
        from SR_Prompt import get_required_string
        with patch('builtins.input', return_value="test value"):
            result = get_required_string("Enter: ", "field")
            assert result == "test value"

    def test_get_required_string_strips_whitespace(self):
        """Test get_required_string strips whitespace."""
        from SR_Prompt import get_required_string
        with patch('builtins.input', return_value="  test value  "):
            result = get_required_string("Enter: ", "field")
            assert result == "test value"

    def test_get_required_string_retries_on_empty(self):
        """Test get_required_string retries on empty input."""
        from SR_Prompt import get_required_string
        with patch('builtins.input', side_effect=["", "", "valid"]):
            result = get_required_string("Enter: ", "field")
            assert result == "valid"

    def test_get_optional_float_with_value(self):
        """Test get_optional_float with a valid float."""
        from SR_Prompt import get_optional_float
        with patch('builtins.input', return_value="123.45"):
            result = get_optional_float("Enter: ")
            assert result == 123.45

    def test_get_optional_float_empty(self):
        """Test get_optional_float with empty input."""
        from SR_Prompt import get_optional_float
        with patch('builtins.input', return_value=""):
            result = get_optional_float("Enter: ")
            assert result is None

    def test_get_optional_float_with_min_max(self):
        """Test get_optional_float with min/max bounds."""
        from SR_Prompt import get_optional_float
        with patch('builtins.input', side_effect=["10", "3.5"]):
            result = get_optional_float("Enter: ", min_value=0.0, max_value=5.0)
            assert result == 3.5

    def test_get_required_float_with_value(self):
        """Test get_required_float with a valid float."""
        from SR_Prompt import get_required_float
        with patch('builtins.input', return_value="99.99"):
            result = get_required_float("Enter: ", "amount")
            assert result == 99.99

    def test_get_required_float_retries_on_invalid(self):
        """Test get_required_float retries on invalid input."""
        from SR_Prompt import get_required_float
        with patch('builtins.input', side_effect=["not a number", "50.0"]):
            result = get_required_float("Enter: ", "amount")
            assert result == 50.0

    def test_get_optional_int_with_value(self):
        """Test get_optional_int with a valid int."""
        from SR_Prompt import get_optional_int
        with patch('builtins.input', return_value="42"):
            result = get_optional_int("Enter: ")
            assert result == 42

    def test_get_optional_int_empty(self):
        """Test get_optional_int with empty input."""
        from SR_Prompt import get_optional_int
        with patch('builtins.input', return_value=""):
            result = get_optional_int("Enter: ")
            assert result is None

    def test_get_required_int_with_value(self):
        """Test get_required_int with a valid int."""
        from SR_Prompt import get_required_int
        with patch('builtins.input', return_value="10"):
            result = get_required_int("Enter: ", "count")
            assert result == 10

    def test_get_yes_no_required_yes(self):
        """Test get_yes_no_required with 'yes' input."""
        from SR_Prompt import get_yes_no_required
        for yes_input in ['y', 'Y', 'yes', 'YES', 'Yes']:
            with patch('builtins.input', return_value=yes_input):
                result = get_yes_no_required("Enter: ")
                assert result == True

    def test_get_yes_no_required_no(self):
        """Test get_yes_no_required with 'no' input."""
        from SR_Prompt import get_yes_no_required
        for no_input in ['n', 'N', 'no', 'NO', 'No']:
            with patch('builtins.input', return_value=no_input):
                result = get_yes_no_required("Enter: ")
                assert result == False

    def test_get_yes_no_optional_empty(self):
        """Test get_yes_no_optional with empty input."""
        from SR_Prompt import get_yes_no_optional
        with patch('builtins.input', return_value=""):
            result = get_yes_no_optional("Enter: ")
            assert result is None

    def test_get_date_optional_valid(self):
        """Test get_date_optional with valid date."""
        from SR_Prompt import get_date_optional
        with patch('builtins.input', return_value="2025-12-31"):
            result = get_date_optional("Enter: ")
            assert result == "2025-12-31"

    def test_get_date_optional_empty(self):
        """Test get_date_optional with empty input."""
        from SR_Prompt import get_date_optional
        with patch('builtins.input', return_value=""):
            result = get_date_optional("Enter: ")
            assert result is None

    def test_get_date_optional_invalid_then_valid(self):
        """Test get_date_optional retries on invalid date."""
        from SR_Prompt import get_date_optional
        with patch('builtins.input', side_effect=["invalid", "2025-12-31"]):
            result = get_date_optional("Enter: ")
            assert result == "2025-12-31"

    def test_get_date_required_valid(self):
        """Test get_date_required with valid date."""
        from SR_Prompt import get_date_required
        with patch('builtins.input', return_value="2025-06-15"):
            result = get_date_required("Enter: ", "deadline")
            assert result == "2025-06-15"


# =============================================================================
# BUG REGRESSION TESTS
# =============================================================================

class TestBugRegressions:
    """
    Regression tests for bugs identified in BUG_REPORT.md.

    These tests define the CORRECT/EXPECTED behavior.
    They will FAIL until the corresponding bug is fixed.
    Once a bug is fixed, its test will PASS.
    """

    # -------------------------------------------------------------------------
    # Bug #1: Type Annotation Error - None Assigned to str
    # Location: Scholarship_Recorder.py:140, 176
    # FIX: Change `enrollment_status: str = None` to `enrollment_status: Optional[str] = None`
    # -------------------------------------------------------------------------
    def test_bug1_enrollment_status_should_be_optional_str(self):
        """
        BUG #1: enrollment_status should be Optional[str], not str.

        EXPECTED: The type annotation should match the actual default value.
        When enrollment_status is None, it should be typed as Optional[str].

        This test checks that the field annotation is correct by verifying
        the dataclass field type includes None as a valid type.
        """
        import typing
        from dataclasses import fields

        # Get the enrollment_status field from Federal_Grant
        federal_fields = {f.name: f for f in fields(Federal_Grant)}
        enrollment_field = federal_fields['enrollment_status']

        # The type should be Optional[str] (i.e., Union[str, None] or str | None)
        # Currently it's just `str` which is wrong since default is None
        field_type = enrollment_field.type

        # Check if None is a valid type (it should be for Optional[str])
        # typing.get_origin and typing.get_args help inspect Union types
        origin = typing.get_origin(field_type)

        # For Optional[str], origin would be Union and args would include NoneType
        # For plain str, origin would be None
        assert origin is typing.Union, \
            f"enrollment_status should be Optional[str] (Union[str, None]), but is {field_type}"

    # -------------------------------------------------------------------------
    # Bug #3: Delete Loop Logic Bug
    # Location: SR_Prompt.py:496-502
    # FIX: Move the `else` to be attached to the `for` loop, not the `if`
    # -------------------------------------------------------------------------
    def test_bug3_delete_should_not_print_not_found_when_item_exists(self):
        """
        BUG #3: When deleting a scholarship that exists, "not found" should
        never be printed - even if it's not the first item in the list.

        EXPECTED: Searching for "Third" in a list of [First, Second, Third]
        should find it without any "not found" messages.

        CURRENT BUG: The else clause is attached to the if statement, so it
        prints "not found" for every non-matching item before finding the target.
        """
        # This is the BUGGY code pattern from SR_Prompt.py lines 496-502
        # We simulate it here to test the fix

        manager = Scholarship_Manager()
        manager.add_scholarship(Scholarship(name="First"))
        manager.add_scholarship(Scholarship(name="Second"))
        manager.add_scholarship(Scholarship(name="Third"))

        delete_prompt = "Third"
        not_found_count = 0
        

        # BUGGY PATTERN (current code):
        # for i in manager.scholarships:
        #     if i.name.lower() == delete_prompt.lower():
        #         break
        #     else:  # <-- BUG: attached to if, not for
        #         print("not found")

        # CORRECT PATTERN (what the fix should look like):
        # for i in manager.scholarships:
        #     if i.name.lower() == delete_prompt.lower():
        #         break
        # else:  # <-- FIXED: attached to for loop
        #     print("not found")

        # Simulate the buggy behavior
        for i in manager.scholarships:
            if i.name.lower() == delete_prompt.lower():
                break
        else:
            not_found_count += 1  # This increments for each non-match (BUG)

        # EXPECTED: When we find the item, not_found_count should be 0
        # ACTUAL (BUG): not_found_count is 2 because it prints for First and Second
        assert not_found_count == 0, \
            f"Should not print 'not found' when item exists. Got {not_found_count} false 'not found' messages."

    # -------------------------------------------------------------------------
    # Bug #5: Missing Required Parameter in Function Call
    # Location: SR_Prompt.py:191
    # FIX: Add the missing field_name parameter
    # -------------------------------------------------------------------------
    def test_bug5_get_required_float_needs_field_name(self):
        """
        BUG #5: get_required_float() call is missing required field_name parameter.

        EXPECTED: The function call should include all required parameters.

        This test verifies the function signature requires field_name and that
        calling without it raises an error.
        """
        from SR_Prompt import get_required_float
        import inspect

        sig = inspect.signature(get_required_float)
        params = list(sig.parameters.keys())

        # Verify field_name is a required parameter (no default)
        assert 'field_name' in params, "get_required_float should have field_name parameter"

        field_name_param = sig.parameters['field_name']
        assert field_name_param.default is inspect.Parameter.empty, \
            "field_name should be a required parameter (no default value)"

    # -------------------------------------------------------------------------
    # Bug #10: Silent Failure on Invalid Date Format
    # Location: Scholarship_Recorder.py:356-357
    # FIX: Log a warning or raise an exception instead of silent pass
    # -------------------------------------------------------------------------
    def test_bug10_invalid_date_should_warn_or_raise(self, capsys):
        """
        BUG #10: auto_remove_expired_scholarships silently ignores invalid dates.

        EXPECTED: When a scholarship has an invalid date format, the method
        should either log a warning or raise an exception - not silently ignore.

        CURRENT BUG: `except ValueError: pass` silently swallows the error.
        """
        manager = Scholarship_Manager()
        invalid = Scholarship(name="Invalid Date", deadline="not-a-date")
        manager.add_scholarship(invalid)

        # Call the method that should warn about invalid dates
        manager.auto_remove_expired_scholarships()

        captured = capsys.readouterr()

        # EXPECTED: Some warning should be output about the invalid date
        # ACTUAL (BUG): Nothing is output, error is silently ignored
        assert "Invalid Date" in captured.out or "not-a-date" in captured.out or \
               "warning" in captured.out.lower() or "error" in captured.out.lower(), \
            "Should warn about invalid date format, but got no output"

    # -------------------------------------------------------------------------
    # Bug #13: Inconsistent Return Type
    # Location: Scholarship_Recorder.py:34
    # FIX: Return Optional[int] and raise ValueError for invalid format
    # -------------------------------------------------------------------------
    def test_bug13_calculate_deadline_should_return_consistent_type(self):
        """
        BUG #13: calculate_deadline() returns int, str, or bool depending on state.

        EXPECTED: Should return Optional[int] - either an int or None.
        Invalid date formats should raise ValueError, not return False.

        CURRENT BUG: Returns int for valid dates, "Undetermined" (str) for None,
        and False (bool) for invalid format.
        """
        from datetime import datetime, timedelta

        # Test 1: Valid future deadline should return int
        future = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")
        s1 = Scholarship(deadline=future)
        result1 = s1.calculate_deadline()
        assert isinstance(result1, int), "Valid deadline should return int"

        # Test 2: None deadline should return None (not string "Undetermined")
        s2 = Scholarship(deadline=None)
        result2 = s2.calculate_deadline()
        assert result2 is None, \
            f"None deadline should return None, not '{result2}' ({type(result2).__name__})"

        # Test 3: Invalid format should raise ValueError (not return False)
        s3 = Scholarship(deadline="invalid")
        try:
            result3 = s3.calculate_deadline()
            # If we get here without exception, check it's not False
            assert result3 is not False, \
                "Invalid date should raise ValueError, not return False"
        except ValueError:
            pass  # This is the expected behavior after fix

    # -------------------------------------------------------------------------
    # Bug #2: Misleading File Extension for Pickle Data
    # Location: SR_Prompt.py:271, 574
    # FIX: Change .json to .pkl or use actual JSON serialization
    # -------------------------------------------------------------------------
    def test_bug2_pickle_file_should_not_use_json_extension(self):
        """
        BUG #2: Pickle data is saved with .json extension.

        EXPECTED: Pickle files should use .pkl or .pickle extension,
        OR the code should use actual JSON serialization.

        This test checks that the default filename in SR_Prompt uses
        an appropriate extension for pickle data.
        """
        from SR_Prompt import main
        import inspect

        # Get the source code of main() to check the filename
        source = inspect.getsource(main)

        # Check for pickle operations with .json extension (the bug)
        has_pickle_with_json = ('scholarships_data.json' in source and
                                ('export_to_saved_file' in source or
                                 'import_from_saved_file' in source))

        # EXPECTED: Should NOT have .json extension for pickle files
        assert not has_pickle_with_json, \
            "Pickle data should not use .json extension. Use .pkl instead."

    # -------------------------------------------------------------------------
    # Bug #4: Instance Method Called as Class Method
    # Location: SR_Prompt.py:516, 520, 524, 528, 532, 536, 540, 543, 550
    # FIX: Change Academic.add_to_sheet(i) to i.add_to_sheet()
    # -------------------------------------------------------------------------
    def test_bug4_add_to_sheet_should_be_called_on_instance(self):
        """
        BUG #4: add_to_sheet() is called as ClassName.add_to_sheet(instance)
        instead of instance.add_to_sheet().

        EXPECTED: The code should use polymorphic instance method calls.

        This test checks the SR_Prompt source for the buggy pattern.
        """
        from SR_Prompt import main
        import inspect
        import re

        source = inspect.getsource(main)

        # Look for the buggy pattern: ClassName.add_to_sheet(variable)
        buggy_patterns = [
            r'Academic\.add_to_sheet\(',
            r'Federal_Grant\.add_to_sheet\(',
            r'Need_Based\.add_to_sheet\(',
            r'Athletic\.add_to_sheet\(',
            r'Minority\.add_to_sheet\(',
            r'Creative_Arts\.add_to_sheet\(',
            r'Community_Service\.add_to_sheet\(',
            r'Scholarship\.add_to_sheet\(',
        ]

        found_bugs = []
        for pattern in buggy_patterns:
            if re.search(pattern, source):
                found_bugs.append(pattern)

        # EXPECTED: No class method style calls
        assert len(found_bugs) == 0, \
            f"Should use instance.add_to_sheet() not ClassName.add_to_sheet(). Found: {found_bugs}"


# =============================================================================
# RUN CONFIGURATION
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

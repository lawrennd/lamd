"""
Unit tests for the mdlist module.
"""

import os
import sys
import tempfile
from unittest.mock import MagicMock, patch

# Add the parent directory to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pandas as pd

from lamd.mdlist import (
    apply_list_filters,
    coerce_yearish_dates,
    compute_section,
    cvlists_config_dir,
    load_cvlists_interface,
    main,
    value_year,
)
from lamd.util import get_since_year, set_since_year


def _expected_cvlists_from_file_kwargs() -> dict[str, object]:
    config_dir = cvlists_config_dir()
    return {
        "user_file": "cvlists.yml",
        "directory": config_dir,
        "allowed_roots": [config_dir],
    }


class TestMdlist:
    """Test suite for the mdlist module."""

    def setup_method(self):
        """Set up test environment before each test."""
        # Create a temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()

        # Create test data files
        self.test_data = """[
            {
                "title": "Test Talk 1",
                "venue": "Test Conference",
                "year": 2022,
                "month": 6,
                "day": 15,
                "url": "https://example.com/talk1"
            },
            {
                "title": "Test Talk 2",
                "venue": "Another Conference",
                "year": 2023,
                "month": 3,
                "day": 10,
                "url": "https://example.com/talk2"
            }
        ]"""

        self.test_data_path = os.path.join(self.temp_dir.name, "talks.json")
        with open(self.test_data_path, "w") as f:
            f.write(self.test_data)

        # Create a test configuration file
        self.config_content = """
talks:
  listtemplate: talk_item
  preprocessor: clean_date
  augmentor: add_talk_details
  sorter: sort_by_date
  filter: recent_talks

compute:
  preprocessor: []
  augmentor: []
  sorter: []

filter: []
"""
        self.config_path = os.path.join(self.temp_dir.name, "cvlists.yml")
        with open(self.config_path, "w") as f:
            f.write(self.config_content)

    def teardown_method(self):
        """Clean up after each test."""
        # Remove temporary directory and its contents
        self.temp_dir.cleanup()

    def test_since_year_functions(self):
        """Test the set_since_year and get_since_year functions."""
        # Test setting and getting the year
        set_since_year(2020)
        assert get_since_year() == 2020

        # Test changing the year
        set_since_year(2022)
        assert get_since_year() == 2022

        # Test setting to None
        set_since_year(None)
        assert get_since_year() is None

    @patch("sys.argv", ["mdlist", "talks", "-s", "2021", "talks.json"])
    @patch("pandas.to_datetime")
    @patch("lynguine.config.interface.Interface.from_file")
    @patch("builtins.print")
    @patch("referia.assess.data.CustomDataFrame.from_flow")
    @patch("lamd.mdlist.load_template_env")
    def test_main_function(self, mock_load_template, mock_custom_df, mock_print, mock_interface, mock_to_datetime):
        """Test the main function with talks list type."""
        # Mock the current date
        mock_now = pd.Timestamp("2024-03-15")
        mock_to_datetime.return_value = mock_now

        # Mock the interface configuration
        class InterfaceDict(dict):
            def __contains__(self, key):
                return dict.__contains__(self, key)

            def __getitem__(self, key):
                return dict.__getitem__(self, key)

        class TalksDict(dict):
            def __contains__(self, key):
                return key in ["listtemplate", "preprocessor", "augmentor", "sorter", "filter", "input", "talks"]

            def __getitem__(self, key):
                if key == "talks":
                    return self
                return dict.__getitem__(self, key)

        talks_dict = TalksDict(
            {
                "listtemplate": "talk_item",
                "preprocessor": "clean_date",
                "augmentor": "add_talk_details",
                "sorter": "sort_by_date",
                "filter": "recent_talks",
                "input": {},
            }
        )
        interface_dict = InterfaceDict({"talks": talks_dict, "lists": {"talks": talks_dict}})
        mock_interface.return_value = interface_dict

        # Mock the template environment
        mock_env = MagicMock()
        mock_template = MagicMock()
        mock_template.render.return_value = "- Test Talk\n"
        mock_env.get_template.return_value = mock_template
        mock_load_template.return_value = mock_env

        # Mock the CustomDataFrame
        mock_df = pd.DataFrame(
            {
                "title": ["Test Talk 1", "Test Talk 2"],
                "venue": ["Test Conference", "Another Conference"],
                "year": [2022, 2023],
                "month": [6, 3],
                "day": [15, 10],
                "url": ["https://example.com/talk1", "https://example.com/talk2"],
            }
        )
        mock_custom_df_instance = MagicMock()
        mock_custom_df_instance.df = mock_df
        mock_custom_df_instance.to_pandas.return_value = mock_df
        mock_custom_df_instance.preprocess = MagicMock()
        mock_custom_df.return_value = mock_custom_df_instance

        # Run the main function
        main()

        mock_interface.assert_called_once_with(**_expected_cvlists_from_file_kwargs())
        import lamd as lamd_pkg

        expected_template_dir = os.path.join(os.path.dirname(os.path.abspath(lamd_pkg.__file__)), "templates")
        mock_load_template.assert_called_once_with(ext=".md", template_dir=expected_template_dir)
        mock_custom_df.assert_called_once()
        mock_custom_df_instance.preprocess.assert_called_once()

        # Verify the output
        expected_output = "- Test Talk\n\n- Test Talk\n\n"
        mock_print.assert_called_once_with(expected_output)

    def test_cvlists_path_construction(self):
        """Test that cvlists.yml path is constructed correctly from package location."""
        import lamd.mdlist as mdlist_module

        # Get the actual path construction logic
        lamd_dir = os.path.dirname(os.path.abspath(mdlist_module.__file__))
        config_dir = os.path.join(lamd_dir, "config")
        cvlists_path = os.path.join(config_dir, "cvlists.yml")

        # Verify the path points to the config directory
        assert config_dir.endswith("lamd/config")
        assert cvlists_path.endswith("lamd/config/cvlists.yml")
        assert os.path.basename(config_dir) == "config"

    @patch("sys.argv", ["mdlist", "talks", "-s", "2021", "talks.json"])
    @patch("pandas.to_datetime")
    @patch("lynguine.config.interface.Interface.from_file")
    @patch("builtins.print")
    @patch("referia.assess.data.CustomDataFrame.from_flow")
    @patch("lamd.mdlist.load_template_env")
    @patch("os.getcwd")
    def test_cvlists_path_independent_of_cwd(
        self, mock_getcwd, mock_load_template, mock_custom_df, mock_print, mock_interface, mock_to_datetime
    ):
        """Test that cvlists.yml is found regardless of current working directory."""
        # Mock different working directories
        mock_getcwd.return_value = "/some/random/directory"

        # Mock the current date
        mock_now = pd.Timestamp("2024-03-15")
        mock_to_datetime.return_value = mock_now

        # Mock the interface configuration
        class InterfaceDict(dict):
            def __contains__(self, key):
                return dict.__contains__(self, key)

            def __getitem__(self, key):
                return dict.__getitem__(self, key)

        class TalksDict(dict):
            def __contains__(self, key):
                return key in ["listtemplate", "preprocessor", "augmentor", "sorter", "filter", "input", "talks"]

            def __getitem__(self, key):
                if key == "talks":
                    return self
                return dict.__getitem__(self, key)

        talks_dict = TalksDict(
            {
                "listtemplate": "talk_item",
                "preprocessor": "clean_date",
                "augmentor": "add_talk_details",
                "sorter": "sort_by_date",
                "filter": "recent_talks",
                "input": {},
            }
        )
        interface_dict = InterfaceDict({"talks": talks_dict, "lists": {"talks": talks_dict}})
        mock_interface.return_value = interface_dict

        # Mock the template environment
        mock_env = MagicMock()
        mock_template = MagicMock()
        mock_template.render.return_value = "- Test Talk\n"
        mock_env.get_template.return_value = mock_template
        mock_load_template.return_value = mock_env

        # Mock the CustomDataFrame
        mock_df = pd.DataFrame(
            {
                "title": ["Test Talk 1"],
                "venue": ["Test Conference"],
                "year": [2022],
            }
        )
        mock_custom_df_instance = MagicMock()
        mock_custom_df_instance.df = mock_df
        mock_custom_df_instance.preprocess = MagicMock()
        mock_custom_df.return_value = mock_custom_df_instance

        # Run the main function
        main()

        assert mock_interface.called, "Interface.from_file should have been called"
        mock_interface.assert_called_once_with(**_expected_cvlists_from_file_kwargs())

    @patch("sys.argv", ["mdlist", "publications", "test1.md", "test2.md"])
    @patch("pandas.to_datetime")
    @patch("lynguine.config.interface.Interface.from_file")
    @patch("builtins.print")
    @patch("referia.assess.data.CustomDataFrame.from_flow")
    @patch("lamd.mdlist.load_template_env")
    def test_index_field_set_in_interface(
        self, mock_load_template, mock_custom_df, mock_print, mock_interface, mock_to_datetime
    ):
        """Test that the index field is set to 'filename' in the interface input configuration."""
        # Mock the current date
        mock_now = pd.Timestamp("2024-03-15")
        mock_to_datetime.return_value = mock_now

        # Create a mock interface that tracks changes to the input configuration
        class InterfaceDict(dict):
            def __contains__(self, key):
                return dict.__contains__(self, key)

            def __getitem__(self, key):
                return dict.__getitem__(self, key)

        class PublicationsDict(dict):
            def __contains__(self, key):
                return key in ["listtemplate", "compute", "input", "publications"]

            def __getitem__(self, key):
                if key == "publications":
                    return self
                return dict.__getitem__(self, key)

        publications_dict = PublicationsDict(
            {
                "listtemplate": "listpaper",
                "compute": {
                    "preprocessor": [],
                    "augmentor": [],
                    "sorter": [],
                },
                "input": {},
            }
        )
        interface_dict = InterfaceDict({"publications": publications_dict})
        mock_interface.return_value = interface_dict

        # Mock the template environment
        mock_env = MagicMock()
        mock_template = MagicMock()
        mock_template.render.return_value = "- Test Publication\n"
        mock_env.get_template.return_value = mock_template
        mock_load_template.return_value = mock_env

        # Mock the CustomDataFrame
        mock_df = pd.DataFrame(
            {
                "title": ["Test Publication 1", "Test Publication 2"],
                "year": [2022, 2023],
            }
        )
        mock_custom_df_instance = MagicMock()
        mock_custom_df_instance.df = mock_df
        mock_custom_df_instance.preprocess = MagicMock()
        mock_custom_df.return_value = mock_custom_df_instance

        # Create test files in temp directory
        test_file1 = os.path.join(self.temp_dir.name, "test1.md")
        test_file2 = os.path.join(self.temp_dir.name, "test2.md")
        with open(test_file1, "w") as f:
            f.write("# Test 1\n")
        with open(test_file2, "w") as f:
            f.write("# Test 2\n")

        # Update sys.argv to use the test files
        import sys

        original_argv = sys.argv
        sys.argv = ["mdlist", "publications", test_file1, test_file2]

        try:
            # Run the main function
            main()
        finally:
            sys.argv = original_argv

        # Verify that CustomDataFrame.from_flow was called
        assert mock_custom_df.called, "CustomDataFrame.from_flow should have been called"

        # Get the interface that was passed to CustomDataFrame.from_flow
        call_args = mock_custom_df.call_args
        passed_interface = call_args[0][0] if call_args[0] else None

        # Verify the interface has the index field set
        assert passed_interface is not None, "Interface should have been passed to CustomDataFrame.from_flow"
        assert "input" in passed_interface, "Interface should have an 'input' key"
        assert "index" in passed_interface["input"], "Interface input should have an 'index' field"
        assert (
            passed_interface["input"]["index"] == "filename"
        ), f"Index field should be set to 'filename', got '{passed_interface['input']['index']}'"

    @patch("sys.argv", ["mdlist", "talks", "talk1.md"])
    @patch("pandas.to_datetime")
    @patch("lynguine.config.interface.Interface.from_file")
    @patch("builtins.print")
    @patch("referia.assess.data.CustomDataFrame.from_flow")
    @patch("lamd.mdlist.load_template_env")
    def test_index_field_set_for_single_file(
        self, mock_load_template, mock_custom_df, mock_print, mock_interface, mock_to_datetime
    ):
        """Test that the index field is set correctly when processing a single file."""
        # Mock the current date
        mock_now = pd.Timestamp("2024-03-15")
        mock_to_datetime.return_value = mock_now

        # Create a mock interface
        class InterfaceDict(dict):
            def __contains__(self, key):
                return dict.__contains__(self, key)

            def __getitem__(self, key):
                return dict.__getitem__(self, key)

        class TalksDict(dict):
            def __contains__(self, key):
                return key in ["listtemplate", "compute", "input", "talks"]

            def __getitem__(self, key):
                if key == "talks":
                    return self
                return dict.__getitem__(self, key)

        talks_dict = TalksDict(
            {
                "listtemplate": "listtalk",
                "compute": {
                    "preprocessor": [],
                    "augmentor": [],
                    "sorter": [],
                },
                "input": {},
            }
        )
        interface_dict = InterfaceDict({"talks": talks_dict})
        mock_interface.return_value = interface_dict

        # Mock the template environment
        mock_env = MagicMock()
        mock_template = MagicMock()
        mock_template.render.return_value = "- Test Talk\n"
        mock_env.get_template.return_value = mock_template
        mock_load_template.return_value = mock_env

        # Mock the CustomDataFrame
        mock_df = pd.DataFrame(
            {
                "title": ["Test Talk"],
                "venue": ["Test Conference"],
                "year": [2022],
            }
        )
        mock_custom_df_instance = MagicMock()
        mock_custom_df_instance.df = mock_df
        mock_custom_df_instance.preprocess = MagicMock()
        mock_custom_df.return_value = mock_custom_df_instance

        # Create test file in temp directory
        test_file = os.path.join(self.temp_dir.name, "talk1.md")
        with open(test_file, "w") as f:
            f.write("# Test Talk\n")

        # Update sys.argv to use the test file
        import sys

        original_argv = sys.argv
        sys.argv = ["mdlist", "talks", test_file]

        try:
            # Run the main function
            main()
        finally:
            sys.argv = original_argv

        # Verify that CustomDataFrame.from_flow was called
        assert mock_custom_df.called, "CustomDataFrame.from_flow should have been called"

        # Get the interface that was passed to CustomDataFrame.from_flow
        call_args = mock_custom_df.call_args
        passed_interface = call_args[0][0] if call_args[0] else None

        # Verify the interface has the index field set
        assert passed_interface is not None, "Interface should have been passed to CustomDataFrame.from_flow"
        assert "input" in passed_interface, "Interface should have an 'input' key"
        assert "index" in passed_interface["input"], "Interface input should have an 'index' field"
        assert (
            passed_interface["input"]["index"] == "filename"
        ), f"Index field should be set to 'filename', got '{passed_interface['input']['index']}'"


def test_load_cvlists_interface_from_other_cwd(tmp_path, monkeypatch) -> None:
    """Package cvlists.yml must load when cwd is a CV directory (lynguine path jail)."""
    monkeypatch.chdir(tmp_path)
    iface = load_cvlists_interface()
    assert "publications" in iface
    assert os.path.isfile(os.path.join(cvlists_config_dir(), "cvlists.yml"))


def test_value_year_accepts_int_datetime_and_string() -> None:
    assert value_year(1998) == 1998
    assert value_year(pd.Timestamp("2020-06-01")) == 2020
    assert value_year("2018-09-03") == 2018
    assert value_year(None) is None


def test_apply_list_filters_since_year_drops_old_publications() -> None:
    df = pd.DataFrame({"title": ["old", "new"], "year": [1998, 2024]})
    mask = apply_list_filters(
        df,
        {"function": "recent", "args": {"column": "year"}},
        since_year=2020,
        today=pd.Timestamp("2026-10-23"),
    )
    assert list(df.loc[mask, "title"]) == ["new"]


def test_apply_list_filters_current_versus_former_grants() -> None:
    today = pd.Timestamp("2026-10-23")
    df = pd.DataFrame(
        {
            "title": ["running", "finished", "year-int-old"],
            "end": [pd.Timestamp("2027-01-01"), pd.Timestamp("2022-12-31"), 2020],
        }
    )
    current = apply_list_filters(df, {"function": "current", "args": {"end": "end"}}, None, today)
    former = apply_list_filters(df, {"function": "former", "args": {"end": "end"}}, None, today)
    assert list(df.loc[current, "title"]) == ["running"]
    assert list(df.loc[former, "title"]) == ["finished", "year-int-old"]


def test_apply_list_filters_explicit_since_without_recent_spec() -> None:
    df = pd.DataFrame({"title": ["old", "new"], "year": [2018, 2022]})
    mask = apply_list_filters(df, [], since_year=2020, today=pd.Timestamp("2026-10-23"), apply_since=True)
    assert list(df.loc[mask, "title"]) == ["new"]


def test_compute_section_unwraps_from_flow_list() -> None:
    mapping = {"sorter": {"function": "descending"}, "filter": {"function": "former"}}
    assert compute_section({"compute": mapping}) == mapping
    assert compute_section({"compute": [mapping]}) == mapping
    assert compute_section({"compute": []}) == {}


def test_current_flag_column_overrides_end_date() -> None:
    today = pd.Timestamp("2026-10-23")
    df = pd.DataFrame(
        {
            "title": ["flagged-current", "flagged-former"],
            "current": [True, False],
            "end": [pd.Timestamp("2020-01-01"), pd.Timestamp("2028-01-01")],
        }
    )
    spec = {"function": "current", "args": {"current": "current", "end": "end"}}
    current = apply_list_filters(df, spec, None, today)
    former = apply_list_filters(df, {"function": "former", "args": {"current": "current", "end": "end"}}, None, today)
    assert list(df.loc[current, "title"]) == ["flagged-current"]
    assert list(df.loc[former, "title"]) == ["flagged-former"]


def test_current_keeps_open_ended_and_nan_end() -> None:
    today = pd.Timestamp("2026-10-23")
    df = pd.DataFrame({"title": ["open", "nan-end", "done"], "end": [pd.NaT, float("nan"), pd.Timestamp("2022-01-01")]})
    current = apply_list_filters(df, {"function": "current", "args": {"end": "end"}}, None, today)
    former = apply_list_filters(df, {"function": "former", "args": {"end": "end"}}, None, today)
    assert list(df.loc[current, "title"]) == ["open", "nan-end"]
    assert list(df.loc[former, "title"]) == ["done"]


def test_coerce_yearish_dates_makes_liquid_safe_timestamps() -> None:
    df = pd.DataFrame(
        {
            "start": [2016, pd.Timestamp("2022-02-07"), 2021],
            "end": [2020, pd.Timestamp("2024-02-06"), float("nan")],
        }
    )
    out = coerce_yearish_dates(df)
    assert out.loc[0, "start"] == pd.Timestamp("2016-01-01")
    assert out.loc[0, "end"] == pd.Timestamp("2020-12-31")
    assert out.loc[1, "start"] == pd.Timestamp("2022-02-07")
    assert pd.isna(out.loc[2, "end"])


def test_coerce_yearish_dates_makes_mixed_dates_sortable() -> None:
    import datetime

    df = pd.DataFrame(
        {
            "start": [2016, datetime.date(2022, 2, 7), pd.Timestamp("2021-01-01")],
            "end": [2020, datetime.date(2024, 2, 6), float("nan")],
        }
    )
    out = coerce_yearish_dates(df)
    sorted_df = out.sort_values(by=["start", "end"], ascending=False, na_position="last")
    assert list(sorted_df["start"]) == [
        pd.Timestamp("2022-02-07"),
        pd.Timestamp("2021-01-01"),
        pd.Timestamp("2016-01-01"),
    ]


def test_list_templates_render_without_reserved_with() -> None:
    from liquid import Environment, FileSystemLoader
    from liquid.exceptions import LiquidSyntaxError, TemplateNotFoundError

    template_dir = os.path.join(os.path.dirname(os.path.abspath(__import__("lamd").__file__)), "templates")
    env = Environment(loader=FileSystemLoader(template_dir))
    teaching = env.get_template("listteaching.md").render(
        title="Advanced Data Science",
        description="Part II unit.",
        start=pd.Timestamp("2021-10-01"),
        end=pd.Timestamp("2024-12-10"),
        collaborators=[{"given": "Ada", "family": "Lovelace"}],
    )
    assert "Advanced Data Science" in teaching
    assert "Ada Lovelace" in teaching
    person = env.get_template("liststudent.md").render(given="Ada", family="Lovelace")
    assert "Ada Lovelace" in person
    grant = env.get_template("listgrant.md").render(
        title="Example Grant",
        currency="£",
        amount=100,
        start=pd.Timestamp("2016-01-01"),
        end=pd.Timestamp("2020-12-31"),
        funders="EPSRC",
        role="PI",
    )
    assert "2016" in grant
    assert "1970" not in grant
    assert "\\n" not in grant
    try:
        env.get_template("listteaching.md")
    except (LiquidSyntaxError, TemplateNotFoundError) as err:
        raise AssertionError(err) from err

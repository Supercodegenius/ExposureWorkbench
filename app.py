import hashlib
from decimal import Decimal

import pandas as pd
import streamlit as st
from treaty import render_treaty

from reinsured_lines import (
    ReinsuredWorkbook,
    ValidationSummary,
    WorkbookFormatError,
    read_generic_workbook,
    validate_metadata,
    validate_rows,
)


st.set_page_config(
    page_title="Exposure Workbench",
    page_icon="A",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        :root {
            --alps-navy: #12304a;
            --alps-blue: #1769aa;
            --alps-muted: #65758b;
            --alps-border: #e4eaf0;
            --alps-surface: #ffffff;
            --alps-background: #f4f7fb;
        }

        [data-testid="stAppViewContainer"] {
            background: var(--alps-background);
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        [data-testid="stSidebar"] {
            background: var(--alps-surface);
            border-right: 1px solid var(--alps-border);
        }

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
            color: var(--alps-muted);
        }

        .brand {
            align-items: center;
            display: flex;
            gap: 0.75rem;
            margin: 0.25rem 0 1.75rem;
        }

        .brand-mark {
            align-items: center;
            background: var(--alps-navy);
            border-radius: 0.65rem;
            color: white;
            display: flex;
            font-size: 1.1rem;
            font-weight: 750;
            height: 2.5rem;
            justify-content: center;
            width: 2.5rem;
        }

        .brand-name {
            color: var(--alps-navy);
            font-size: 1.05rem;
            font-weight: 700;
            line-height: 1.2;
        }

        .brand-caption {
            color: var(--alps-muted);
            font-size: 0.75rem;
            margin-top: 0.2rem;
        }

        .nav-caption {
            color: var(--alps-muted);
            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 0.09em;
            margin: 0 0 0.5rem 0.25rem;
            text-transform: uppercase;
        }

        [data-testid="stSidebar"] .stButton > button {
            border: 0;
            border-radius: 0.55rem;
            color: #34465a;
            min-height: 2.7rem;
            text-align: left;
        }

        [data-testid="stSidebar"] .stButton > button[kind="primary"] {
            background: #eaf3fb;
            color: var(--alps-blue);
            font-weight: 650;
        }

        .page-eyebrow {
            color: var(--alps-blue);
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            margin-bottom: 0.35rem;
            text-transform: uppercase;
        }

        .page-title {
            color: var(--alps-navy);
            font-size: 2rem;
            font-weight: 720;
            letter-spacing: -0.025em;
            margin: 0;
        }

        .page-description {
            color: var(--alps-muted);
            font-size: 1rem;
            margin-top: 0.45rem;
        }

        .welcome-card,
        .module-card {
            background: var(--alps-surface);
            border: 1px solid var(--alps-border);
            border-radius: 0.9rem;
            padding: 1.5rem;
        }

        .welcome-card {
            border-left: 4px solid var(--alps-blue);
        }

        .welcome-card h2,
        .module-card h2 {
            color: var(--alps-navy);
            font-size: 1.15rem;
            margin: 0 0 0.5rem;
        }

        .welcome-card p,
        .module-card p {
            color: var(--alps-muted);
            line-height: 1.55;
            margin: 0;
        }

        .section-label {
            color: var(--alps-navy);
            font-size: 1.05rem;
            font-weight: 650;
            margin-bottom: 0.75rem;
        }

        .status-pill {
            background: #edf2f7;
            border-radius: 99px;
            color: #526579;
            display: inline-block;
            font-size: 0.75rem;
            font-weight: 600;
            margin-top: 1rem;
            padding: 0.3rem 0.65rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

if "page" not in st.session_state:
    st.session_state.page = "Home"

with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-mark">A</div>
            <div>
                <div class="brand-name">Exposure</div>
                <div class="brand-caption">Workbench</div>
            </div>
        </div>
        <div class="nav-caption">Workspace</div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "Home",
        key="nav_home",
        type="primary" if st.session_state.page == "Home" else "secondary",
        use_container_width=True,
    ):
        st.session_state.page = "Home"
        st.rerun()

    if st.button(
        "Import Reinsured Lines",
        key="nav_reinsured_lines",
        type="primary" if st.session_state.page == "Import Reinsured Lines" else "secondary",
        use_container_width=True,
    ):
        st.session_state.page = "Import Reinsured Lines"
        st.rerun()

    if st.button(
        "Treaty",
        key="nav_treaty",
        type="primary" if st.session_state.page == "Treaty" else "secondary",
        use_container_width=True,
    ):
        st.session_state.page = "Treaty"
        st.rerun()

    if st.button(
        "Exposure Reporting",
        key="nav_exposure_reporting",
        type="primary" if st.session_state.page == "Exposure Reporting" else "secondary",
        use_container_width=True,
    ):
        st.session_state.page = "Exposure Reporting"
        st.rerun()

if st.session_state.page == "Home":
    st.markdown('<div class="page-eyebrow">Workspace</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="page-title">Home</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="page-description">Your starting point for ALPS data migration tasks.</p>',
        unsafe_allow_html=True,
    )
    st.write("")

    st.markdown(
        """
        <section class="welcome-card">
            <h2>Welcome to Exposure Workbench</h2>
            <p>
                Choose a task from the navigation menu to get started.
                The first workspace is <strong>Import Reinsured Lines</strong>.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    st.markdown('<div class="section-label">Available workspace</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <section class="module-card">
            <h2>Import Reinsured Lines</h2>
            <p>Open the reinsured lines import workspace.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Open Import Reinsured Lines", type="primary", key="open_reinsured_lines"):
        st.session_state.page = "Import Reinsured Lines"
        st.rerun()

    st.write("")
    st.markdown(
        """
        <section class="module-card">
            <h2>Exposure Reporting</h2>
            <p>Open the exposure reporting workspace.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Open Exposure Reporting", type="primary", key="open_exposure_reporting"):
        st.session_state.page = "Exposure Reporting"
        st.rerun()
elif st.session_state.page == "Treaty":
    render_treaty()
elif st.session_state.page == "Exposure Reporting":
    st.markdown('<div class="page-eyebrow">Reporting</div>', unsafe_allow_html=True)
    st.markdown(
        '<h1 class="page-title">Exposure Reporting</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="page-description">Your workspace for exposure reports.</p>',
        unsafe_allow_html=True,
    )
    st.write("")
    st.info(
        "Exposure Reporting is ready for report configuration. "
        "Report generation and data connections are not implemented yet."
    )
else:
    st.markdown('<div class="page-eyebrow">Import</div>', unsafe_allow_html=True)
    st.markdown(
        '<h1 class="page-title">Import Reinsured Lines</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="page-description">Validate a Generic / other Lines of Business workbook and review an import dry run.</p>',
        unsafe_allow_html=True,
    )
    st.write("")

    st.warning(
        "Dry-run only: this page does not connect to ALPS or write to a database. "
        "ALPS reference-data checks, subject resolution, duplicate/overlap detection, "
        "and database updates are not performed."
    )
    line_of_business = st.selectbox(
        "Line of Business",
        (
            "Generic / Other",
            "Casualty",
            "Credit and Political Risks",
        ),
        help="Casualty and Credit/Political Risks allow comma-separated cover types.",
    )
    uploaded_file = st.file_uploader(
        "Choose a Reinsured Lines workbook",
        type=("xlsx", "xlsm"),
        help="Use the ALPS Generic Reinsured Lines import template (.xlsx or .xlsm).",
    )

    current_digest = None
    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()
        current_digest = hashlib.sha256(file_bytes).hexdigest()
        st.caption(f"Selected workbook: {uploaded_file.name}")
        if len(file_bytes) > 25 * 1024 * 1024:
            st.error("The workbook exceeds the 25 MB upload limit.")
            current_digest = None
        if st.session_state.get("reinsured_validated_digest") != current_digest:
            st.session_state.pop("reinsured_workbook", None)
            st.session_state.pop("reinsured_validation", None)
            st.session_state.pop("reinsured_metadata_errors", None)
            st.session_state.pop("reinsured_dry_run", None)
    else:
        st.session_state.pop("reinsured_workbook", None)
        st.session_state.pop("reinsured_validation", None)
        st.session_state.pop("reinsured_metadata_errors", None)
        st.session_state.pop("reinsured_dry_run", None)
        st.session_state.pop("reinsured_validated_digest", None)

    validate_clicked = st.button(
        "Validate Data",
        type="primary",
        disabled=uploaded_file is None or current_digest is None,
        key="validate_reinsured_lines",
    )
    if validate_clicked and uploaded_file is not None and current_digest is not None:
        try:
            parsed_workbook = read_generic_workbook(file_bytes)
            metadata_errors, normalized_as_at = validate_metadata(
                parsed_workbook.reinsured,
                parsed_workbook.as_at,
            )
            summary = validate_rows(parsed_workbook.rows, line_of_business)
            st.session_state["reinsured_workbook"] = parsed_workbook
            st.session_state["reinsured_validation"] = summary
            st.session_state["reinsured_metadata_errors"] = metadata_errors
            st.session_state["reinsured_as_at"] = normalized_as_at
            st.session_state["reinsured_validated_digest"] = current_digest
            st.session_state["reinsured_validated_lob"] = line_of_business
            st.session_state.pop("reinsured_validation_error", None)
            st.session_state.pop("reinsured_dry_run", None)
        except WorkbookFormatError as exc:
            st.session_state["reinsured_validation_error"] = str(exc)
            st.session_state.pop("reinsured_workbook", None)
            st.session_state.pop("reinsured_validation", None)
        except Exception as exc:
            st.session_state["reinsured_validation_error"] = (
                f"Unable to validate the workbook: {exc}"
            )
            st.session_state.pop("reinsured_workbook", None)
            st.session_state.pop("reinsured_validation", None)
    elif current_digest != st.session_state.get("reinsured_validated_digest"):
        st.session_state.pop("reinsured_validation_error", None)

    if st.session_state.get("reinsured_validation_error"):
        st.error(st.session_state["reinsured_validation_error"])

    workbook: ReinsuredWorkbook | None = st.session_state.get("reinsured_workbook")
    validation: ValidationSummary | None = st.session_state.get("reinsured_validation")
    metadata_errors: list[str] = st.session_state.get(
        "reinsured_metadata_errors", []
    )
    if workbook is not None and validation is not None:
        st.divider()
        st.subheader("Validation results")
        if st.session_state.get("reinsured_validated_lob") != line_of_business:
            st.session_state.pop("reinsured_dry_run", None)
        st.write(
            f"**Reinsured:** {workbook.reinsured or 'Not provided'}　"
            f"**As at:** {st.session_state.get('reinsured_as_at') or 'Not provided'}"
        )
        if st.session_state.get("reinsured_validated_lob") != line_of_business:
            st.info("Line of Business changed. Select Validate Data to rerun checks.")

        count_columns = st.columns(4)
        count_columns[0].metric("Rows", len(validation.rows))
        count_columns[1].metric(
            "Validation errors",
            validation.error_count + len(metadata_errors),
        )
        count_columns[2].metric("Rows with warnings", validation.warning_count)
        count_columns[3].metric(
            "Eligible for dry run",
            validation.import_count if not metadata_errors else 0,
        )
        for error in metadata_errors:
            st.error(error)

        if not validation.rows:
            st.error("No Reinsured Lines data rows were found in the workbook.")
        else:
            result_rows = []
            for result in validation.rows:
                result_rows.append(
                    {
                        "Excel row": result.excel_row,
                        "Result": (
                            "Error"
                            if result.errors
                            else "Skipped"
                            if result.ignored
                            else "Ready"
                        ),
                        "Subject": result.values.get("Subject"),
                        "Cover type": result.values.get("CoverType"),
                        "Currency": result.values.get("Ccy"),
                        "Inception": result.values.get("Inception"),
                        "Expiry": result.values.get("Expiry"),
                        "Line %": result.values.get("LinePer"),
                        "Interest %": result.values.get("InterestPercent"),
                        "Status": result.values.get("Status"),
                        "Errors": " ".join(result.errors),
                        "Warnings": " ".join(result.warnings),
                    }
                )
            st.dataframe(
                pd.DataFrame(result_rows),
                hide_index=True,
                use_container_width=True,
            )

        can_dry_run = (
            validation.valid
            and validation.import_count > 0
            and not metadata_errors
            and st.session_state.get("reinsured_validated_lob") == line_of_business
            and current_digest == st.session_state.get("reinsured_validated_digest")
        )
        if st.button(
            "Import Data (Dry Run)",
            type="primary",
            disabled=not can_dry_run,
            key="dry_run_reinsured_lines",
        ):
            st.session_state["reinsured_dry_run"] = True

        if st.session_state.get("reinsured_dry_run"):
            import_rows = [
                {
                    key: (str(value) if isinstance(value, Decimal) else value)
                    for key, value in result.values.items()
                }
                for result in validation.rows
                if result.can_import
            ]
            preview = pd.DataFrame(import_rows)
            st.success(
                f"Dry run complete: {len(import_rows)} line(s) are eligible. "
                "No data was written to ALPS."
            )
            st.dataframe(preview, hide_index=True, use_container_width=True)
            st.download_button(
                "Download dry-run preview (CSV)",
                data=preview.to_csv(index=False).encode("utf-8-sig"),
                file_name="reinsured_lines_dry_run.csv",
                mime="text/csv",
                key="download_reinsured_dry_run",
            )

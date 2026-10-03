import streamlit as st
from pipeline import run_research


st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🔎",
    layout="wide"
)


st.title("🔎 AI Research Agent")
st.caption("Search → Scrape → Write → Critic")


topic = st.text_input(
    "Research Topic",
    placeholder="e.g. Impact of AI on software development"
)


if st.button("🚀 Start Research", type="primary"):

    if not topic.strip():
        st.warning("Please enter a research topic.")
    else:

        with st.spinner("AI agents are researching..."):

            try:
                state = run_research(topic)

                st.success("Research completed successfully!")

                st.divider()

                tab1, tab2, tab3, tab4 = st.tabs(
                    [
                        "🔎 Search Results",
                        "📄 Scraped Content",
                        "📝 Final Report",
                        "🔍 Critic Feedback"
                    ]
                )

                with tab1:
                    st.subheader("Search Results")
                    st.write(state["search_results"])

                with tab2:
                    st.subheader("Scraped Content")
                    st.write(state["scraped_content"])

                with tab3:
                    st.subheader("Final Report")
                    st.markdown(state["report"])

                with tab4:
                    st.subheader("Critic Feedback")
                    st.write(state["feedback"])

            except Exception as e:
                st.error("Something went wrong.")
                st.exception(e)
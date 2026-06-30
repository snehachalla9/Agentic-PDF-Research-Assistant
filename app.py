import streamlit as st

# ============================================
# AUTHENTICATION IMPORTS - ADD THIS SECTION AT THE TOP
# ============================================
from auth.session import (
    initialize_session,
    check_authentication,
    is_logged_in,
    get_user,
    clear_session
)
from auth.auth import logout
from auth.login import login_page
from auth.sign_up import signup_page
from database.db import (
    create_conversation,
    get_conversations,
    save_chat,
    get_chat_history
)
from database.supabase import supabase

# ============================================
# EXISTING IMPORTS - KEEP AS IS
# ============================================
from utils.pdf_loader import load_pdf
from utils.chunker import create_chunks
from utils.embeddings import create_embeddings
from utils.vector_store import create_vectorstore
from utils.llm import generate_answer
from utils.memory import get_chat_history as get_memory_history

# Import LangGraph components
from graph import build_research_graph


# ============================================
# EXISTING CONFIGURATION - KEEP AS IS
# ============================================

# Task mapping for display names to internal task names
TASK_MAPPING = {
    "Ask Questions": "question_answering",
    "Summarize Paper": "summary",
    "Research Gaps": "research_gap",
    "Compare Papers": "comparison",
    "Literature Review": "literature_review",
    "Generate Citations": "citation"
}

# Reverse mapping for display
TASK_DISPLAY = {v: k for k, v in TASK_MAPPING.items()}


# ============================================
# HELPER FUNCTION FOR USER ATTRIBUTE ACCESS
# ============================================

def get_user_attribute(user, attr, default=None):
    """
    Safely get attribute from user object whether it's a dict or object.
    """
    if user is None:
        return default
    
    # If it's a dictionary
    if isinstance(user, dict):
        return user.get(attr, default)
    
    # If it's an object
    try:
        return getattr(user, attr, default)
    except:
        return default


# ============================================
# EXISTING FALLBACK SINGLE-AGENT MODE - KEEP AS IS
# ============================================

def fallback_single_agent(query, task, db, chunks, doc_sources):
    """
    Fallback to the original single-agent RAG pipeline
    if the multi-agent system fails.
    """
    try:
        # Import all required modules inside the function
        from utils.retriver import retrieve_documents
        from utils.hybrid_retriver import hybrid_retrieve
        from utils.reranker import rerank_documents
        from utils.prompt import build_prompt
        from utils.summary_prompt import build_summary_prompt
        from utils.research_gap_prompt import build_research_gap_prompt
        from utils.comparison_prompt import build_comparison_prompt
        from utils.literature_review_prompt import build_literature_review_prompt
        from utils.citation_prompt import build_citation_prompt
        
        # Prompt builder registry
        PROMPT_BUILDERS = {
            "Ask Questions": build_prompt,
            "Summarize Paper": build_summary_prompt,
            "Research Gaps": build_research_gap_prompt,
            "Compare Papers": build_comparison_prompt,
            "Literature Review": build_literature_review_prompt,
            "Generate Citations": build_citation_prompt
        }
        
        # Task-specific retrieval configurations
        TASK_CONFIGS = {
            "Ask Questions": {"retrieval_k": 20, "rerank_k": None},
            "Summarize Paper": {"retrieval_k": None, "rerank_k": None},
            "Research Gaps": {"retrieval_k": 20, "rerank_k": None},
            "Compare Papers": {"retrieval_k": 30, "rerank_k": 15},
            "Literature Review": {"retrieval_k": 40, "rerank_k": 20},
            "Generate Citations": {"retrieval_k": 25, "rerank_k": 12}
        }
        
        # Determine if using all chunks
        use_all_chunks = task == "Summarize Paper"
        query_text = "Summarize this paper" if use_all_chunks else query
        
        # Build context
        if use_all_chunks:
            # Handle Document objects for chunks
            context_parts = []
            for chunk in chunks:
                if hasattr(chunk, 'page_content'):
                    context_parts.append(chunk.page_content)
                elif isinstance(chunk, dict):
                    context_parts.append(chunk.get("page_content", ""))
                else:
                    context_parts.append(str(chunk))
            context = "\n\n".join(context_parts)
            docs_found = chunks
        else:
            config = TASK_CONFIGS.get(task, {"retrieval_k": 20, "rerank_k": None})
            retrieval_k = config.get("retrieval_k", 20)
            rerank_k = config.get("rerank_k", 3)
            
            # Use hybrid search by default
            docs_found = hybrid_retrieve(
                vector_store=db,
                chunks=chunks,
                query=query_text,
                k=retrieval_k
            )
            
            docs_found = rerank_documents(
                query=query_text,
                docs=docs_found,
                top_k=rerank_k if rerank_k else 3
            )
            
            # Handle Document objects for context
            context_parts = []
            for doc in docs_found:
                if hasattr(doc, 'page_content'):
                    context_parts.append(doc.page_content)
                elif isinstance(doc, dict):
                    context_parts.append(doc.get("page_content", ""))
                else:
                    context_parts.append(str(doc))
            context = "\n\n".join(context_parts)
        
        # Build prompt
        history = get_memory_history(st.session_state.messages)
        prompt_builder = PROMPT_BUILDERS.get(task)
        
        if prompt_builder:
            prompt = prompt_builder(
                query=query_text,
                context=context,
                history=history,
                sources=doc_sources if task in ["Compare Papers", "Literature Review", "Generate Citations"] else None
            )
            
            answer = generate_answer(prompt)
            
            # Display in chat
            with st.chat_message("user"):
                st.write(query)
            with st.chat_message("assistant"):
                st.write(answer)
            
            # Save to history
            if len(st.session_state.messages) == 0 or st.session_state.messages[-1]["question"] != query:
                st.session_state.messages.append({
                    "question": query,
                    "answer": answer
                })
            
            return True  # Success
        else:
            st.error(f"No prompt builder found for task: {task}")
            return False
            
    except Exception as e:
        st.error(f"❌ Fallback error: {str(e)}")
        st.write("Please try again or re-upload your documents.")
        return False


# ============================================
# SESSION STATE - MODIFY THIS SECTION
# ============================================

# Initialize session - ADD THIS AT THE VERY START
initialize_session()

# Check authentication - ADD THIS RIGHT AFTER initialize_session()
check_authentication()

if not is_logged_in():
    # ============================================
    # FIX 1: Add Login/Signup navigation - REPLACE login_page() with this
    # ============================================
    st.sidebar.title("🔐 Authentication")
    auth_page = st.sidebar.radio(
        "Choose an option",
        ["Login", "Sign Up"],
        index=0
    )
    
    if auth_page == "Login":
        login_page()
    else:
        signup_page()
    
    st.stop()  # Stop execution here to prevent showing the app

# If we reach here, user is logged in
# Get user info - FIX 2: Use safe attribute access
user = get_user()
user_email = get_user_attribute(user, "email", "Unknown User")
user_id = get_user_attribute(user, "id", None)

# Initialize app-specific session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "graph" not in st.session_state:
    st.session_state.graph = None

# ADD THESE NEW SESSION STATE VARIABLES
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None

if "current_conversation" not in st.session_state:
    st.session_state.current_conversation = None

if "loaded_conversation" not in st.session_state:
    st.session_state.loaded_conversation = False

# ============================================
# FIX 3: Load conversations directly (no caching)
# ============================================
if user_id:
    st.session_state.conversations = get_conversations(user_id)
else:
    st.session_state.conversations = []


# ============================================
# UI HEADER - KEEP AS IS
# ============================================

st.title("Advanced PDF RAG Assistant - Multi-Agent")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message("user"):
        st.write(msg["question"])
    with st.chat_message("assistant"):
        st.write(msg["answer"])


# ============================================
# SIDEBAR - MODIFY THIS SECTION
# ============================================

with st.sidebar:
    # ============================================
    # ADD USER INFO AND LOGOUT - INSERT AT TOP OF SIDEBAR
    # ============================================
    st.header("👤 User")
    st.write(f"Logged in as: **{user_email}**")
    
    if st.button("🚪 Logout", use_container_width=True):
        logout()
        clear_session()
        st.rerun()
    
    st.divider()
    
    # ============================================
    # ADD CONVERSATION HISTORY - INSERT AFTER LOGOUT BUTTON
    # ============================================
    st.header("💬 Conversations")
    
    # Display conversations - always fresh from database
    if st.session_state.conversations:
        for conv in st.session_state.conversations:
            # Create a button for each conversation
            if st.button(
                f"📝 {conv['title']}",
                key=f"conv_{conv['id']}",
                use_container_width=True
            ):
                # Load selected conversation
                conversation_id = conv['id']
                chat_history = get_chat_history(conversation_id)
                
                # Update session state
                st.session_state.messages = [
                    {
                        "question": msg['question'],
                        "answer": msg['answer'],
                        "task": msg.get('task', 'Ask Questions')
                    }
                    for msg in chat_history
                ]
                st.session_state.conversation_id = conversation_id
                st.session_state.current_conversation = conv['title']
                st.session_state.loaded_conversation = True
                
                st.rerun()
    else:
        st.info("No conversations yet. Start chatting!")
    
    st.divider()
    
    # ============================================
    # EXISTING SIDEBAR CONTENT - KEEP AS IS
    # ============================================
    st.header("⚙️ Configuration")
    chunk_size = st.slider("Chunk Size", 200, 2000, 1000)
    chunk_overlap = st.slider("Chunk Overlap", 0, 500, 100)
    
    st.divider()
    st.header("🔍 Research Task")
    task = st.selectbox(
        "Select Task",
        [
            "Ask Questions",
            "Summarize Paper",
            "Research Gaps",
            "Compare Papers",
            "Literature Review",
            "Generate Citations"
        ]
    )
    
    st.divider()
    st.header("📊 Agent Status")
    if st.session_state.graph:
        st.success("✅ Multi-Agent System Ready")
        st.info("Agents: Planner → Retriever → Research → Answer")
    else:
        st.warning("⚠️ Upload a PDF to initialize agents")


# ============================================
# FILE UPLOAD - KEEP AS IS
# ============================================

uploaded_files = st.file_uploader(
    "📄 Upload PDF",
    type="pdf",
    accept_multiple_files=True
)

query = st.chat_input("Ask about your documents...")


# ============================================
# PROCESS UPLOADED FILES - MODIFY THIS SECTION
# ============================================

if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} PDFs Uploaded")
    all_docs = []
    doc_sources = []

    # Save and load each PDF
    for pdf in uploaded_files:
        with open(pdf.name, "wb") as f:
            f.write(pdf.read())
        docs = load_pdf(pdf.name)
        for doc in docs:
            doc.metadata['source'] = pdf.name
        all_docs.extend(docs)
        doc_sources.append(pdf.name)

    st.write(f"📚 Total pages: {len(all_docs)}")
    st.write(f"📂 Documents: {', '.join(doc_sources)}")

    # Chunking
    with st.spinner("🔄 Creating chunks..."):
        chunks = create_chunks(all_docs, chunk_size, chunk_overlap)
    
    # Add metadata to chunks
    for chunk in chunks:
        title = chunk.metadata.get("title", "")
        author = chunk.metadata.get("author", "")
        doi = chunk.metadata.get("doi", "")
        source = chunk.metadata.get("source", "")
        chunk.page_content = f"""
        Source: {source}
        Title: {title}
        Author: {author}
        DOI: {doi}
{chunk.page_content}
"""
    
    st.write(f"📦 Chunks created: {len(chunks)}")
    
    # Debug view
    show_chunks = st.checkbox("Show Debug Chunks")
    if show_chunks:
        st.subheader("All Chunks")
        for i, chunk in enumerate(chunks[:5]):  # Show first 5 only
            st.write(f"Chunk {i+1}")
            st.write(chunk.metadata)
            st.write(chunk.page_content[:300])
            st.divider()

    # Embeddings and Vector Store
    with st.spinner("🧠 Creating embeddings and vector store..."):
        embeddings = create_embeddings()
        db = create_vectorstore(chunks, embeddings)
    
    st.success("✅ Vector database ready!")
    
    # Build and cache the graph
    with st.spinner("🔗 Building multi-agent graph..."):
        if st.session_state.graph is None:
            st.session_state.graph = build_research_graph()
    
    st.info(f"🎯 Current Task: {task}")
    st.info("🤖 Multi-Agent Mode: Active")


    # ============================================
    # PROCESS REQUEST USING MULTI-AGENT SYSTEM - MODIFY THIS SECTION
    # ============================================
    
    if query:
        # Map display task to internal task name
        internal_task = TASK_MAPPING.get(task, "question_answering")
        
        with st.spinner("🧠 Processing with Multi-Agent System..."):
            
            # Create progress tracking
            progress_placeholder = st.empty()
            progress_placeholder.info("🤖 Planner Agent: Analyzing query...")
            
            # Prepare initial state for the graph
            initial_state = {
                "query": query,
                "task": internal_task,  # Will be overridden by planner
                "plan": [],
                "db": db,
                "chunks": chunks,
                "retrieved_docs": [],
                "research_output": "",
                "final_answer": ""
            }
            
            # Update progress
            progress_placeholder.info("🔍 Retriever Agent: Finding relevant documents...")
            
            try:
                # Execute the multi-agent workflow (graph is a function)
                result = st.session_state.graph(initial_state)
                
                # Update progress
                progress_placeholder.info("📚 Research Agent: Analyzing documents...")
                
                # Get the final answer
                answer = result.get("final_answer", "No answer generated.")
                task_display = TASK_DISPLAY.get(result.get("task", "question_answering"), "Ask Questions")
                
                # Get retrieved documents for sources
                docs_found = result.get("retrieved_docs", [])
                
                # Clear progress
                progress_placeholder.empty()
                
                # Display in chat
                with st.chat_message("user"):
                    st.write(query)
                with st.chat_message("assistant"):
                    st.write(answer)
                
                # ============================================
                # SAVE TO DATABASE - ADD THIS BLOCK
                # ============================================
                # Create a conversation if this is the first message
                if st.session_state.conversation_id is None and user_id:
                    # Create a new conversation with the first few words of the query
                    title = query[:50] + "..." if len(query) > 50 else query
                    result_data = create_conversation(user_id, title)
                    
                    # Extract conversation ID from response
                    if result_data and len(result_data) > 0:
                        conversation_id = result_data[0]['id']
                        st.session_state.conversation_id = conversation_id
                        st.session_state.current_conversation = title
                        
                        # Reload conversations list - FIX 3: Always refresh
                        st.session_state.conversations = get_conversations(user_id)
                
                # Save the chat to database
                if st.session_state.conversation_id and user_id:
                    save_chat(
                        conversation_id=st.session_state.conversation_id,
                        user_id=user_id,
                        question=query,
                        answer=answer,
                        task=task_display
                    )
                # ============================================
                
                # Save to session state history
                if len(st.session_state.messages) == 0 or st.session_state.messages[-1]["question"] != query:
                    st.session_state.messages.append({
                        "question": query,
                        "answer": answer,
                        "task": task_display,
                        "docs": docs_found
                    })
                
                # ============================================
                # SHOW SOURCES AND AGENT TRACE - KEEP AS IS
                # ============================================
                
                with st.expander("📚 Sources & Agent Trace"):
                    # Show agent execution trace
                    st.subheader("🤖 Agent Execution Trace")
                    st.write(f"**Query:** {query}")
                    st.write(f"**Task:** {task_display}")
                    st.write(f"**Plan:** {result.get('plan', [])}")
                    
                    st.divider()
                    
                    # Show retrieval stats - FIXED for Document objects
                    st.subheader("📄 Retrieved Documents")
                    if docs_found:
                        st.write(f"**Total documents retrieved:** {len(docs_found)}")
                        seen = set()
                        for i, doc in enumerate(docs_found[:10]):
                            # Handle Document objects
                            if hasattr(doc, 'metadata'):
                                source = doc.metadata.get("source", "Unknown")
                                page = doc.metadata.get("page", 0)
                            elif isinstance(doc, dict):
                                source = doc.get("metadata", {}).get("source", "Unknown")
                                page = doc.get("metadata", {}).get("page", 0)
                            else:
                                source = "Unknown"
                                page = 0
                            
                            if (source, page) not in seen:
                                st.write(f"{i+1}. 📄 {source} | Page {page+1}")
                                seen.add((source, page))
                        if len(docs_found) > 10:
                            st.write(f"... and {len(docs_found) - 10} more documents")
                    else:
                        st.write("No documents retrieved.")
                    
                    st.divider()
                    
                    # Show research output
                    st.subheader("🔬 Research Output")
                    research_output = result.get("research_output", "")
                    if research_output:
                        st.text_area("Research Analysis", research_output, height=100)
                    else:
                        st.write("No research output generated.")
                    
                    st.divider()
                    
                    # Show task-specific details
                    st.subheader("📋 Task Details")
                    st.write(f"**Task Type:** {result.get('task', 'unknown')}")
                    st.write(f"**Plan Steps:** {len(result.get('plan', []))}")
                    
            except Exception as e:
                progress_placeholder.empty()
                st.error(f"❌ Error in multi-agent workflow: {str(e)}")
                st.write("Falling back to single-agent mode...")
                
                # Fallback to original single-agent mode
                success = fallback_single_agent(query, task, db, chunks, doc_sources)
                
                if success:
                    # ============================================
                    # SAVE FALLBACK RESPONSE TO DATABASE - ADD THIS BLOCK
                    # ============================================
                    # Get the last message from session state
                    if st.session_state.messages:
                        last_msg = st.session_state.messages[-1]
                        if last_msg.get("question") == query:
                            # Create conversation if needed
                            if st.session_state.conversation_id is None and user_id:
                                title = query[:50] + "..." if len(query) > 50 else query
                                result_data = create_conversation(user_id, title)
                                if result_data and len(result_data) > 0:
                                    conversation_id = result_data[0]['id']
                                    st.session_state.conversation_id = conversation_id
                                    st.session_state.current_conversation = title
                                    # FIX 3: Always refresh conversations
                                    st.session_state.conversations = get_conversations(user_id)
                            
                            # Save to database
                            if st.session_state.conversation_id and user_id:
                                save_chat(
                                    conversation_id=st.session_state.conversation_id,
                                    user_id=user_id,
                                    question=query,
                                    answer=last_msg.get("answer", ""),
                                    task=task
                                )
                    # ============================================
                else:
                    st.error("❌ Both multi-agent and fallback modes failed.")
                    st.write("Please try again or restart the application.")

# If no files uploaded, show instructions
else:
    st.info("👈 Please upload PDF files to get started.")
from database import Task, get_session, create_task
import streamlit as st
from sqlalchemy import select

session = get_session()

# ---------- Add ----------
def add_task():
    st.subheader("Add Task")
    title = st.text_input("Task Title")
    description = st.text_area("Task Description")

    if st.button("Add Task"):
        if title:
            try:
                create_task(title, description)
                st.success("Task added successfully!")
                st.rerun()
            except Exception:
                st.error("Task with this title already exists. Please choose a different title.")
        else:
            st.error("Please fill in the title.")


# ---------- List ----------
def task_list():
    st.subheader("My Tasks")
    stmt = select(Task)
    tasks = session.scalars(stmt).all()
    if tasks:
        for task in tasks:
            col1, col2, col3 = st.columns([4,1,1])
            with col1:
                st.write(f"**Task ID:** {task.id}")
                st.write(f"**Title:** {task.title}")
                st.write(f"**Description:** {task.description}")
            with col2:
                if st.button("🗑️ Delete", key=f"del_{task.id}"):
                    session.delete(task)
                    session.commit()
                    st.success(f"Task {task.title}: deleted successfully.")
                    st.rerun()
            with col3:
                if st.button("✏️ Update", key=f"upd_{task.id}"):
                    st.session_state.edit_task_id = task.id
                    st.session_state.page = "update"
                    st.rerun()
            st.write("----------------------------------")
    else:
        st.write("No tasks found.")


# ---------- Update ----------
def update_task(task_id):
    task = session.get(Task, task_id)
    if not task:
        st.error("Task not found!")
        return

    st.subheader(f"Update Task {task.id}")
    new_title = st.text_input("Title", value=task.title, key="update_title")
    new_desc = st.text_area("Description", value=task.description or "", key="update_desc")

    if st.button("💾 Save Changes"):
        task.title = new_title
        task.description = new_desc
        session.commit()
        st.success("Task updated successfully!")
        st.session_state.page = "view"
        st.rerun()

    if st.button("↩️ Back"):
        st.session_state.page = "view"
        st.rerun()


# ---------- Main ----------
def main():
    if "page" not in st.session_state:
        st.session_state.page = "view"

    st.title("Task Management App")
    menu = ["Add Task", "View My Tasks"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Task":
        st.session_state.page = "add"
    elif choice == "View My Tasks" and st.session_state.page != "update":
        st.session_state.page = "view"

    # --- Routing ---
    if st.session_state.page == "add":
        add_task()
    elif st.session_state.page == "view":
        task_list()
    elif st.session_state.page == "update":
        update_task(st.session_state.edit_task_id)


if __name__ == "__main__":
    main()

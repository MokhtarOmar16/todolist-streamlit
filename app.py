from database import Task, get_session
import streamlit as st

def main():
    st.title("Task Management App")

    session = get_session()

    with session:
        tasks = session.query(Task).all()

        if tasks:
            st.write("Tasks:")
            for task in tasks:
                st.write(f"**{task.title}**: {task.description or 'No description'}")
        else:
            st.write("No tasks found.")


if __name__ == "__main__":
    main()


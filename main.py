import streamlit as st

def main():
    st.title("Welcome to My Streamlit App")
    st.write("This is a simple Streamlit application.")
    
    button = st.button("Click Me")

    if button:
        st.write("Button clicked!")


if __name__ == "__main__":
    main()
    
import streamlit as st
from api.users import User
from api.loan import Loan
from api.books import Book
from api.teaching_materials import TeachingMaterial

loans = Loan().get_all_loans()

def get_loan_color(loan_index):
    colors = ["#FFDDC1", "#C2EABD", "#AED9E0", "#FFD3B5", "#D4A5A5"]
    return colors[loan_index % len(colors)]

st.header('List Loans')


search_term = st.text_input("Search by id, description, category, date acquisition, serie number, etc.")
if loans:
    for index, loan in enumerate(loans):
        loanee_first_name = User(loan.id_user).get_user_by_id().first_name
        book_name = Book(loan.id_book).get_book_by_isbn().title
        if (
            not search_term
            or search_term.lower() in str(loan.id).lower()
            or search_term.lower() in str(loan.id_book).lower()
            or search_term.lower() in str(loan.id_material).lower()
            or search_term.lower() in str(loan.id_user).lower()
            or search_term.lower() in str(loan.loan_date).lower()
            or search_term.lower() in str(loan.expected_return_date).lower()
            or search_term.lower() in loan.status.lower()
            or search_term.lower() in loanee_first_name.lower()
            or search_term.lower() in book_name.lower()
        ):
            background_color = get_loan_color(index)
            
            if loan.id_book is None:
                st.markdown(
                    f'<div style="display: flex; align-items: center; padding: 10px; border-radius: 5px; background-color: {background_color}; color: black">'
                        f'<div style="flex: 1; padding-right: 10px;">'
                            f'<h2 style="color: black">ID: {loan.id}</h2>'
                            f'<div style="display: flex; flex-direction: column; flex-wrap: wrap; margin-left: 20px;">'
                                f'<p>Status: {loan.status}</p>'
                                f'<p>Loan Date: {loan.loan_date}</p>'
                                f'<p>Expected Return Date: {loan.expected_return_date}</p>'
                                f'<p>Teaching Material ID: {loan.id_material}</p>'
                                f'<p>User ID: {loan.id_user}</p>'
                                f'<p>User Name: {User(id_user).id_user.get_user_by_id().first_name}</p>'
                            f'</div>'
                        f'</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
                st.text('')
            else:
                st.markdown(
                    f'<div style="display: flex; align-items: center; padding: 10px; border-radius: 5px; background-color: {background_color}; color: black">'
                        f'<div style="flex: 1; padding-right: 10px;">'
                            f'<h2 style="color: black">ID: {loan.id}</h2>'
                            f'<div style="display: flex; flex-direction: column; flex-wrap: wrap; margin-left: 20px;">'
                                f'<p>Status: {loan.status}</p>'
                                f'<p>Loan Date: {loan.loan_date}</p>'
                                f'<p>Expected Return Date: {loan.expected_return_date}</p>'
                                f'<p>Book ID: {loan.id_book}</p>'
                                f'<p>Book Name: {book_name }</p>'
                                f'<p>Library User ID: {loan.id_user}</p>'
                                f'<p>Library User First Name: {loanee_first_name}</p>'
                            f'</div>'
                        f'</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
                st.text('')
 
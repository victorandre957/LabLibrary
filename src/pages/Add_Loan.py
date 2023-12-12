import streamlit as st
from api.users import User
from api.books import Book
from api.loan import Loan
from api.teaching_materials import TeachingMaterial
import datetime
from globals import logged_user


st.header('Add a New Loan')
LoanTypes = ['BOOK', 'TEACHING_MATERIAL']
BooksId = [book.isbn for book in Book().get_available_books()]
Books = Book().get_available_books()
TeachingMaterialsId = [tm.id for tm in TeachingMaterial().get_available_teaching_materials()]
TeachingMaterials = TeachingMaterial().get_available_teaching_materials()
ObjectType = st.selectbox('Object Type', LoanTypes)

# Diferencia os campos de Livro e Material Didático
if ObjectType == 'BOOK':
    st.write('Book')
    book_id = st.selectbox('Book ISBN', BooksId)
    if BooksId != []:
        st.write("Book Name - " + Book(book_id).get_book_by_isbn().title)
else:
    st.write('Teaching Material')
    teaching_material_id = st.selectbox('Teaching Material ID', TeachingMaterialsId)
    if TeachingMaterialsId != []:
        st.write('Serial Number - ' + TeachingMaterial(teaching_material_id).get_teaching_material_by_id().serie_number)

# Diferencia os campos dependedo do tipo de usuário
loan_date = st.date_input('Loan Date')
if logged_user["role"] == "MEMBER":
    loan_status='IN_PROGRESS'
    id_user = logged_user["id"]
    expected_return_date = datetime.date.today() + datetime.timedelta(days=7) # default - 7 dias a partir da data atual
elif logged_user["role"] == "ADMIN":
    status = st.selectbox('Status', ['BORROWED', 'RETURNED'])
    id_user = st.selectbox('User', [user.id for user in User().get_users()])
    st.write('Name - ' + User(id_user).get_user_by_id().first_name)
    if status == 'BORROWED':
        default_date = datetime.date.today() + datetime.timedelta(days=7)
        expected_return_date = st.date_input('Expected Return Date', default_date)
        loan_status='IN_PROGRESS'
    else: 
        expected_return_date = st.date_input('Return Date')
        loan_status='COMPLETED'


if st.button('Confirm'):
    new_loan = Loan(
        loan_date=loan_date,
        expected_return_date=expected_return_date,
        status=loan_status,
        id_book=book_id if ObjectType == 'BOOK' else None,
        id_material=teaching_material_id if ObjectType == 'TEACHING_MATERIAL' else None,
        id_user=id_user,
    )
    
    if new_loan.create_loan():
        st.success('Loan inserted successfully!')
    else:
        st.error('Error inserting loan.')
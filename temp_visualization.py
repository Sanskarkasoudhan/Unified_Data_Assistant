import streamlit as st
import matplotlib.pyplot as plt

st.title('Visualization')

code_from_gemini = '''
import matplotlib.pyplot as plt

years = ['2020', '2021', '2022']
sales = [236282, 279833, 315880]

fig, ax = plt.subplots()

ax.plot(years, sales, marker='o')

ax.set_xlabel("Year")
ax.set_ylabel("Net Sales (millions of USD)")
ax.set_title("Net Sales in North America")

plt.show()
'''

exec(code_from_gemini, globals())
st.pyplot(fig)

## Title: Explore AI in the Academic World - A Dashboard for Grad School Applicants

## Yeseong Jeon and Ning Liu

## Purpose:
We have created a comprehensive dashboard tailored for computer science graduate students to help them select universities for their applications based on their research interests in AI, defined by five key subjects: Artificial Intelligence, Computer Vision, Natural Language Processing, Machine Learning, and Information Retrieval. <span style="color:red;">(R4, R5)</span>.

## Demo
[https://mediaspace.illinois.edu/media/t/1_xservc6z](#)  

## Installation:
1. Clone the repository: `git clone https://github.com/CS411DSO-SU24/Ning_Yeseong.git`
2. Run the application: `python app.py`
3. Copy and paste the link generated in your terminal (e.g., `http://127.0.0.1:80**/`)

## Usage
**Widget 1**: (Static Widget) shows the percentage of publications related to five AI subjects. This widget will help users pick which AI subject to work on based on its popularity.

**Widget 2**: (Interactive Widget) From the dropdown menu, users can select an AI subject and a university. The widget will show the top 15 professors based on their keyword-relevant citations. This widget provides users with a list of advisor candidates for their grad school studies.

**Widget 3**: (Interactive Widget) Given a professor's name, this widget will display detailed information about that professor, including their contact information and a must-read paper (highly cited and published recently).

**Widget 4**: (Interactive Widget) This widget will provide rankings of universities based on their performance in each AI subject. The ranking is based on the count of key publications, where the key publication is defined as the publication with a score higher than the average. Users can note down their university of interest by writing down the university ID in the notepad, see Widget 6.

**Widget 5**: (Interactive Widget) This widget will showcase the most cited publications in each AI subject. Users can take note of the publications they want to read and add them to their favorite paper list (see Widget 7) by using the publication ID.

**Widget 6**: (Interactive Widget) This notepad widget will allow users to input and keep track of the universities they plan to apply to.

**Widget 7**: (Interactive Widget) This notepad widget will enable users to input and track the papers they need to read.

In summary, we have 7 widgets that take inputs from users <span style="color:red;">(R9)</span> with 2 updating widgets <span style="color:red;">(R10)</span> and 6 interactive widgets <span style="color:red;">(R11)</span>. We designed widgets in rectangular spaces <span style="color:red;">(R12)</span>.

## Design
We have one main `app.py` with frontend implementation using Dash, along with three supporting files: `mongodb_utils.py`, `mysql_utils.py`, and `neo4j_utils.py` to perform queries and interact with each database.

## Implementation
**Widget 1 and 2** are implemented with MySQL <span style="color:red;">(R6)</span>.

**Widget 3** is implemented with MySQL using a View <span style="color:red;">(R6)</span>.

**Widget 4** is implemented with MongoDB <span style="color:red;">(R7)</span>.

**Widget 5** is implemented with Neo4j <span style="color:red;">(R8)</span>.

**Widget 6 and 7** are implemented with MySQL and perform updates (insertion and deletion) using transactions of a backend database. We also created stored procedures to drop existing ones and recreate two temporary tables - favorite university and favorite paper - every time the user is using this dashboard.

## Database Techniques
Our project leverages multiple database techniques in MySQL to achieve an efficient and interactive dashboard:
- **Views**: Used in Widget 3 to provide a simplified and optimized way to fetch and display professor details without complex queries. <span style="color:red;">(R13)</span>
- **Transactions**: Employed in Widgets 6 and 7 to ensure data integrity during insertions and deletions, making user interactions reliable. <span style="color:red;">(R14)</span>
- **Stored Procedures**: Implemented to manage temporary tables for tracking favorite universities and papers, ensuring they are recreated each session for a fresh start. <span style="color:red;">(R15)</span>

## Extra-Credit Capabilities
Not implemented.

## Contributions
We contributed equally to all aspects of the project, including design, implementation, testing, and documentation, with each person spending approximately 20 hours.

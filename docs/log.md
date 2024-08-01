1. first idea

2. Okay, so I have a feeling that this is going to need, I need to make a chatbot for this, and I need to have like a specific database for this, and also I think a part of data analytics also kind of plays a role in this. So yeah, so what kind of skills do I need specifically to make this work? Like data analysis should be done, cleaning should be done, no, no need of cleaning, right? I'm not sure, so can you just give me an idea of what kind of things that I need to learn, and like what kind, what, what are the steps that I need to take, and give me a schedule on what all to take, like can you plan this whole asset project planning thing?

3. Yes, but can you make the project timeline, the schedule so that I make the projects as I learn? Because if you build a project path in a way that I can learn as I go all the things, then it would be beneficial for me as well as I'll be able to learn it more, right? Can you make it a learning-based project planning kind of thing? Project-based learning? Yeah, that's the word. After just giving me an outline of the project, can you tell me the levels of the basic websites, the steps, what the website would look like after each session so I could have a visualization of it? Thank you.




form.<field>.data for formatting in roites.py
in html file
()
.label
.errors
changed the initial databse plan adding or replacing credit/debit with income, expense, loan, reimbursement
- is it a good idea ? think again
26.07.2024
- almosted completed my models.py
- learning the relationship concept in sqlalchemy 
- not sure if WriteOnlyMapped is the right choice cz it doesn't allow quering other fields or smthng 
  I'm not sure but letsee. If it doesn't work I'll change it up then


- so made a overview & layout for the html files/pages needed
- need to make a list of all the viewfns for all the links now 
- need to make a list of all the viewfns for all the links now (webpages_layout.md)

- also made a project overview & future version kinda ideas like model training 
  inspired from my current project for IBM internship d idea ? think again

28.07.2024
- finished model.py
-  **Doubt**
-  - should i add e
     #related_transaction_id: FK
   #transactions:  reln
   # ans trns reln
   #should i make a relnship for related_transaction_id???

   

  
27.07.2024
- got error in flask db migrate & upgrade
OperationalError : unable to open the database file

Here, when i checked, I couldnt see the Users table migrations script that i made or the app.db that should have been created when i did the upgrade command then.

SO yea spent 3 days trying all kinds of things asking chatgpt blackbox stackoverflow even yt & trying various other stuff

& i got the feeling that yea it might be cz the app.db & the initial script is not here 
so maybe the earlier flask db didnt work properly so 
I tried reinstalling flask-migrate but that also kinda failed

So now 30.07.2024
- finally fixed it by making a whole new repo folder & copy pasting code from my past commit from part4 of users & posts table 
then changing themodels to UPTB 
& alhamdulilla IT WORKED!!!

onto the next part
- created the github repo newly from the terminal 
that was also a task in itself kinda cz i ve never tried it before
but yep done 
havto finish this too in 2 days as planned

----------
part 5 from tutorial
- set password werkzeug.security & its 2 fns in models.py
- imported LoginManager from flask_login 

userMixin 4
user loader fn
current_user, login_user, logout_user
login fn
logout fn
- login/logout if fn in base.html

- requiring users to login
login_required next query string
3rd case urlsplit() netloc

01.08.2024
- fixed error in the redirecting from signin login to index (was a bug cz of a ')
- just realizd there was no validation error problem in my code
i just forgot for a momnet what validation was AAGHH
validation means if the data input doesnt match thetype of datatype & properties weve filled out in models
so yep invalid password etc was supposed to vbe flash msg itself haha
validationerror comes for eg if we do not fill in a required field


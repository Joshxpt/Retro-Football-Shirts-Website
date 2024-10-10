from ListItems import app, db, Shirt

retro_shirts = [
    { "name": "Chelsea 1998", "price": "250", "description": "A retro Chelsea shirt from the 1998 UEFA Cup Winners' Cup final worn by iconic players such as Zola, Desailly and Wise.", "image":"chelsea1998.jpg", "environmental_impact": "Low",  "environmental_explanation":"This shirt uses sustainable, paper packaging to make a low environmental impact" },
    { "name": "Real Madrid 2004", "price": "300", "description": "A retro Real Madrid shirt from the 2004/05 season where despite limited success trophy wise, saw players like the great R9 Ronaldo score 20+ goals.", "image":"realmadrid2004.jpg", "environmental_impact": "Moderate", "environmental_explanation":"Whilst this shirt uses organic cotton, it still has a moderate negative effect on the environmental impact." },
    { "name": "AC Milan 1996", "price": "500", "description": "A retro AC Milan shirt from the 1996 season, where they saw a domestic league title and great players such as George Weah wear the iconic shirt.", "image":"acmilan1996.jpg", "environmental_impact": "High", "environmental_explanation":"This shirt has to be imported and therefore has a higher environmental impact." },
    { "name": "FC Barcelona 1980", "price":"750", "description": "A retro FC Barcelona shirt from 1980 where they saw a great win in the Copa Del Rey!", "image":"fcbarcelona1980.jpeg", "environmental_impact": "Moderate", "environmental_explanation":"Whilst this shirt uses organic cotton, it still has a moderate negative effect on the environmental impact." },
    { "name": "Manchester United 1984", "price": "140", "description": "A retro Man Utd shirt from the 1984 season where they managed to win an FA Cup despite recieving a red card against Everton", "image":"manchesterunited1984.jpg", "environmental_impact": "Low", "environmental_explanation":"This shirt was produced using recycled materials and has a low environmental impact" },
    { "name": "Liverpool FC 1996", "price": "560","description": "A retro Liverpool shirt from 1996-98 when Roy Evens was manager with players such as Michael Owen, Robbie Fowler and Jamie Redknapp", "image":"liverpool1996.jpg", "environmental_impact": "High", "environmental_explanation":"This shirt uses conventional cotton rather than organic leading to a high enivronmental impact." }
]


with app.app_context():
    #db.drop_all()  # only un comment when making changes to DB here.
    db.create_all() # creates the empty tables
    
    for shirts in retro_shirts:
        newShirt = Shirt(name=shirts["name"], price=shirts["price"], description=shirts["description"], environmental_impact=shirts["environmental_impact"], environmental_explanation=shirts["environmental_explanation"], image=shirts["image"])
        db.session.add(newShirt)
    
    db.session.commit()


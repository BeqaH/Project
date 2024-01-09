from extensions import db, app, login_manager

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash



class BaseModel:

    def create(self):
        db.session.add(self)
        db.session.commit()


    def save(self):
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()

class User(db.Model, BaseModel, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    role = db.Column(db.String)

    def __init__(self, username, password, role="guest"):
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role

    def check_password(self, password):
        return check_password_hash(self.password, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



class Blog(db.Model, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    image = db.Column(db.String)

# class Comment(db.Model, BaseModel):
#     id = db.Column(db.Integer, primary_key=True)
#     comment = db.Column(db.String, unique=True)
#     blog_id = db.Column(db.Integer, db.Foreignkey('blog.id'), nullable=False)




if __name__ == "__main__":
    blogs = [
        {'image': 'australia.jpg', 'name': 'Australia', 'id': 0,
         'description': 'Australias diversity is mind-blowing. From the Great Barrier Reef to the Outback,each region has its own unique charm. The wildlife is fascinating, and the locals are incredibly friendly. A dream destination for nature lovers! While the experience was amazing, the high cost of living and tourism activities was a downside. Budget travelers may find it challenging. Australia is a once-in-a-lifetime destination, but financial planning is crucial.'},
        {'image': 'brazil.jpg', 'name': 'Brazil', 'id': 1,
         'description': 'Brazils rich cultural tapestry left me in awe. From the vibrant Carnival in Rio to the historic streets of Salvador, every corner tells a unique story. The warmth of the people and the rhythm of samba made this trip unforgettable. The Amazon Rainforest and Iguazu Falls are wonders of nature, and the beaches in Florianopolis are pristine. However, issues like deforestation and pollution were noticeable. Brazils commitment to environmental conservation is crucial for future visits.'},
        {'image': 'hungary.jpg', 'name': 'Hungary', 'id': 2,
         'description': 'Budapests architecture is a masterpiece, especially along the Danube. The thermal baths are a unique experience, and the rich history is captivating. Hungary exceeded my expectations, offering a perfect blend of culture and relaxation. Hungarian cuisine is a highlight. Goulash and chimney cake are a must-try. However, the service in some places was inconsistent. Budapest is fantastic, but smaller towns need more focus on tourism infrastructure.'},
        {'image': 'montenegro.jpg', 'name': 'Montenegro', 'id': 3,
         'description': 'Montenegro is a hidden gem in Europe. The Bay of Kotor is breathtaking, and the old town has an enchanting charm. The hospitality of the locals is heartwarming. However, more investment in infrastructure could enhance the overall tourist experience. The landscapes are stunning, but the crowds in popular spots like Kotor can be overwhelming. The lack of diverse activities beyond the scenery was a drawback. Montenegro has potential, but a more balanced tourism approach is needed.'},
        {'image': 'philippines.jpg', 'name': 'Philippines', 'id': 4,
         'description': 'The Philippines is a true paradise with its crystal-clear waters and white sandy beaches. Palawan and Boracay are postcard-perfect. The hospitality of the Filipinos makes you feel like family. A tropical dream come true! The popularity of places like El Nido and Oslob has led to overcrowding, impacting the natural beauty. Sustainable tourism practices are crucial to preserve the Philippines incredible landscapes for future generations.'},
        {'image': 'sri_lanka.jpg', 'name': 'Sri Lanka', 'id': 5,
         'description': 'Sri Lankas landscapes are serene, from tea plantations to pristine beaches. The cultural sites like Sigiriya and Polonnaruwa are awe-inspiring. Warm hospitality and delicious cuisine added to the overall charm. While the natural beauty is undeniable, infrastructure in some areas needs improvement. Transportation and waste management can be better. Sri Lanka has immense potential but needs sustainable development.'}
    ]


    with app.app_context():
        db.create_all()

        for blog in blogs:
            new_blog = Blog(name=blog["name"], description=blog["description"], image=blog["image"])
            db.session.add(new_blog)
            db.session.commit()

        admin_user = User(username="Admin_User", password="adminpassword", role="admin")
        admin_user.create()
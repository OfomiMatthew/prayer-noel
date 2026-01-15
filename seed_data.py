"""
Seed script to populate the database with sample data
Run this after creating the database to add initial content
"""

from app import create_app
from app.models import db, User, PrayerRequest, Prayer, Encouragement, AdventReflection
from datetime import datetime

def seed_database():
    app = create_app()
    
    with app.app_context():
        # Clear existing data (optional - comment out if you want to keep existing data)
        print("Clearing existing data...")
        db.drop_all()
        db.create_all()
        
        # Create sample users
        print("Creating users...")
        
        # Admin user
        admin = User(username='admin', email='admin@praynoel.com', is_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Regular users
        users_data = [
            ('sarah_hope', 'sarah@example.com', 'password123'),
            ('john_faithful', 'john@example.com', 'password123'),
            ('mary_grace', 'mary@example.com', 'password123'),
            ('david_prayer', 'david@example.com', 'password123'),
            ('ruth_believer', 'ruth@example.com', 'password123'),
        ]
        
        users = []
        for username, email, password in users_data:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            users.append(user)
        
        db.session.commit()
        print(f"Created {len(users) + 1} users")
        
        # Create sample prayer requests
        print("Creating prayer requests...")
        
        prayer_requests_data = [
            {
                'title': 'Healing for My Mother',
                'content': 'My mother was recently diagnosed with a serious illness. We are trusting God for complete healing and restoration. Please pray for strength for our family during this difficult time.',
                'category': 'Health',
                'bible_verse': '"By his wounds we are healed." - Isaiah 53:5',
                'is_urgent': True,
                'user': users[0]
            },
            {
                'title': 'Job Interview This Week',
                'content': 'I have an important job interview coming up that could change my family\'s financial situation. Praying for God\'s favor and peace during the interview process.',
                'category': 'Finances',
                'bible_verse': '"And my God will meet all your needs according to the riches of his glory in Christ Jesus." - Philippians 4:19',
                'is_urgent': False,
                'user': users[1]
            },
            {
                'title': 'Reconciliation with My Sister',
                'content': 'My sister and I haven\'t spoken in years due to a misunderstanding. This Christmas season, I feel called to reach out and restore our relationship. Please pray for wisdom and healing.',
                'category': 'Relationships',
                'bible_verse': '"If it is possible, as far as it depends on you, live at peace with everyone." - Romans 12:18',
                'is_urgent': False,
                'user': users[2]
            },
            {
                'title': 'Grief After Losing My Father',
                'content': 'I lost my father three months ago and the grief is overwhelming. I\'m struggling to find joy this Christmas season. Please pray for comfort and peace.',
                'category': 'Grief',
                'bible_verse': '"Blessed are those who mourn, for they will be comforted." - Matthew 5:4',
                'is_urgent': False,
                'user': users[3]
            },
            {
                'title': 'Thanksgiving for Answered Prayers',
                'content': 'God has been so faithful this year! Our family faced many challenges but He brought us through every single one. I want to give thanks and encourage others to keep believing!',
                'category': 'Gratitude',
                'bible_verse': '"Give thanks to the Lord, for he is good; his love endures forever." - Psalm 107:1',
                'is_urgent': False,
                'is_answered': True,
                'testimony': 'God answered every single prayer this year in ways better than we could imagine. He is faithful!',
                'user': users[4]
            },
            {
                'title': 'Wisdom for Major Life Decision',
                'content': 'I\'m facing a major decision about relocating for work. It would mean leaving my church community and starting over. Praying for clear direction from God.',
                'category': 'Family',
                'bible_verse': '"If any of you lacks wisdom, you should ask God, who gives generously to all without finding fault, and it will be given to you." - James 1:5',
                'is_urgent': False,
                'user': users[0]
            },
            {
                'title': 'Marriage Restoration',
                'content': 'My marriage is going through a very difficult season. We need God\'s intervention and healing. Please pray for restoration and renewed love.',
                'category': 'Relationships',
                'bible_verse': '"Love is patient, love is kind..." - 1 Corinthians 13:4',
                'is_urgent': True,
                'user': users[1]
            },
            {
                'title': 'Financial Breakthrough Needed',
                'content': 'We\'re facing unexpected medical bills and I\'m worried about making ends meet. Trusting God to provide but feeling overwhelmed.',
                'category': 'Finances',
                'bible_verse': '"Cast all your anxiety on him because he cares for you." - 1 Peter 5:7',
                'is_urgent': True,
                'user': users[2]
            }
        ]
        
        prayer_requests = []
        for req_data in prayer_requests_data:
            request = PrayerRequest(
                title=req_data['title'],
                content=req_data['content'],
                category=req_data['category'],
                bible_verse=req_data.get('bible_verse'),
                is_urgent=req_data.get('is_urgent', False),
                is_answered=req_data.get('is_answered', False),
                testimony=req_data.get('testimony'),
                user_id=req_data['user'].id,
                is_public=True,
                created_at=datetime.utcnow()
            )
            db.session.add(request)
            prayer_requests.append(request)
        
        db.session.commit()
        print(f"Created {len(prayer_requests)} prayer requests")
        
        # Create prayers
        print("Creating prayers...")
        prayers_count = 0
        for request in prayer_requests[:6]:  # Add prayers to first 6 requests
            for user in users[:3]:  # Each of first 3 users prays
                if user.id != request.user_id:  # Don't pray for own request
                    prayer = Prayer(
                        user_id=user.id,
                        request_id=request.id,
                        prayer_note="Praying for you! God is faithful." if prayers_count % 3 == 0 else None,
                        is_private=False
                    )
                    db.session.add(prayer)
                    prayers_count += 1
        
        db.session.commit()
        print(f"Created {prayers_count} prayers")
        
        # Create encouragements
        print("Creating encouragements...")
        encouragements_data = [
            {
                'request_idx': 0,
                'user_idx': 2,
                'content': "I'm standing with you in prayer for your mother's healing. God is the Great Physician!",
                'bible_verse': '"He heals the brokenhearted and binds up their wounds." - Psalm 147:3'
            },
            {
                'request_idx': 1,
                'user_idx': 3,
                'content': "Trust in God's timing and plan for your career. He has good things in store for you!",
                'bible_verse': '"For I know the plans I have for you, declares the Lord, plans to prosper you..." - Jeremiah 29:11'
            },
            {
                'request_idx': 2,
                'user_idx': 0,
                'content': "Reconciliation is such a beautiful gift. May God give you the right words and the right timing.",
                'bible_verse': None
            }
        ]
        
        for enc_data in encouragements_data:
            encouragement = Encouragement(
                user_id=users[enc_data['user_idx']].id,
                request_id=prayer_requests[enc_data['request_idx']].id,
                content=enc_data['content'],
                bible_verse=enc_data.get('bible_verse')
            )
            db.session.add(encouragement)
        
        db.session.commit()
        print(f"Created {len(encouragements_data)} encouragements")
        
        # Create Advent Reflections (sample for first few days)
        print("Creating advent reflections...")
        advent_data = [
            {
                'day': 1,
                'scripture': '"Therefore the Lord himself will give you a sign: The virgin will conceive and give birth to a son, and will call him Immanuel." - Isaiah 7:14',
                'reflection': 'The promise of Emmanuel - God with us - was prophesied hundreds of years before Jesus\' birth. Today, reflect on how God is with you in this season.',
                'prompt': 'Where do you need to experience God\'s presence today?'
            },
            {
                'day': 2,
                'scripture': '"But the angel said to them, \'Do not be afraid. I bring you good news that will cause great joy for all the people.\'" - Luke 2:10',
                'reflection': 'The angels brought good news of great joy. In a world full of anxiety, the birth of Jesus reminds us that God brings joy even in difficult circumstances.',
                'prompt': 'What fears can you surrender to God today?'
            },
            {
                'day': 3,
                'scripture': '"For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life." - John 3:16',
                'reflection': 'Christmas is the ultimate expression of God\'s love. He gave His most precious gift because of His great love for us.',
                'prompt': 'How can you share God\'s love with someone today?'
            },
            {
                'day': 24,
                'scripture': '"And she gave birth to her firstborn, a son. She wrapped him in cloths and placed him in a manger, because there was no guest room available for them." - Luke 2:7',
                'reflection': 'On Christmas Eve, we remember the humble birth of our Savior. The King of Kings was born in a stable, reminding us that God often works in unexpected ways.',
                'prompt': 'How is God working in unexpected ways in your life?'
            },
            {
                'day': 25,
                'scripture': '"Today in the town of David a Savior has been born to you; he is the Messiah, the Lord." - Luke 2:11',
                'reflection': 'Christmas Day! The promise is fulfilled. Our Savior is born. Let us rejoice and celebrate the greatest gift ever given.',
                'prompt': 'How will you celebrate Jesus today?'
            }
        ]
        
        for adv_data in advent_data:
            reflection = AdventReflection(
                day=adv_data['day'],
                scripture=adv_data['scripture'],
                reflection=adv_data['reflection'],
                prompt=adv_data['prompt']
            )
            db.session.add(reflection)
        
        db.session.commit()
        print(f"Created {len(advent_data)} advent reflections")
        
        print("\n✅ Database seeded successfully!")
        print("\n📝 Login credentials:")
        print("   Admin: admin@praynoel.com / admin123")
        print("   User 1: sarah@example.com / password123")
        print("   User 2: john@example.com / password123")
        print("\n🌐 Start the app with: python run.py")
        print("   Then visit: http://localhost:5000")

if __name__ == '__main__':
    seed_database()

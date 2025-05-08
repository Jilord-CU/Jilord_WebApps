from app import app, db, Technology

technologies = [
    { "number": "0", "image": "/static/metro.jpg", "name": "Metro Rimless Close Coupled Modern Toilet", "price": "£189.95", "description": "To give your bathroom an up-to-the-minute look opt for this Modern Toilet from Metro. It's a close coupled toilet, meaning the cistern is attached to the bowl as a single unit. The sleek pan is easy to keep clean. With a projection of 650mm, this neat and compact piece won't hog space in smaller bathrooms. It's supplied with a wrap-over seat that has soft-close hinges – great for preserving your peaceful bathroom ambience. Its rimless design, with no hidden areas for germs to linger, makes it a more hygienic choice." },
    { "number": "1", "image": "/static/bidet.jpg", "name": "Back to Wall Smart Bidet Japanese Toilet", "price": "£599.97", "description": "Experience the future of comfort and hygiene with the Back-to-Wall Smart Bidet Japanese Toilet. Designed for sleek sophistication, this toilet seamlessly fits against your wall, creating a modern, clean look while maximizing space. Equipped with advanced features, including a heated seat, adjustable water temperature, and a built-in bidet for a gentle, soothing cleanse, it offers unparalleled convenience. The intelligent, touchless controls allow for a personalized experience, while the self-cleaning system ensures long-lasting freshness." },
    { "number": "2", "image": "/static/gold-toilet.jpg", "name": "Court Art Style Luxury Bathroom Toilet Seat Golden Split Piece Toilet", "price": "£1781.99", "description": "Transform your bathroom into a palace with the Golden Toilet. Featuring a stunning gold-plated finish, this luxurious toilet combines elegance and advanced flushing technology. Its sleek design offers both comfort and efficiency, while the durable gold coating resists stains and tarnish. Perfect for those who want to add a touch of opulence to their space." },
    { "number": "3", "image": "/static/concrete-toilet.jpg", "name": "Nipomo in Ash", "price": "£721", "description": "Adaptable? Check. Resourceful? Absolutely. Stunning? See for yourself! This concrete bathroom sink is perfect for clean design styles, in oh-so-many ways. Install as an apron-front sink, undermount sink or vessel sink; its soft rectangular shape shows off the organic beauty of NativeStone concrete, at a much lighter weight and with no-fuss maintenance." },
    { "number": "4", "image": "/static/washbasin.jpg", "name": "Furniture Washbasin", "price": "£179.99", "description": "This furniture washbasin has an especially spacious design, providing enough room for your most important accessories. The furniture washbasin can be combined with washbasin countertops or furniture in any style of bath making it the right choice to create a comfortable atmosphere in your bathroom." },
    { "number": "5", "image": "/static/rectangle-sink.jpg", "name": "Ceramic Washbasin", "price": "£224.99", "description": "A ceramic washbasin combines elegance and durability, offering a smooth, glossy surface that resists stains and scratches. Its timeless design fits seamlessly into any bathroom or powder room, providing both style and functionality for everyday use. Ideal for creating a clean, modern aesthetic, this washbasin is easy to maintain and built to last." }
]

with app.app_context():
    db.create_all()

    for tech in technologies:
        newTech = Technology(name = tech["name"], price=tech["price"], description=tech["description"])
        db.session.add(newTech)

    db.session.commit()
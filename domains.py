from models import dalle_image_table
from dalle import generate_images


async def answer_bot(session, user_id, prompt):
    url = generate_images(prompt)
    await session.execute(dalle_image_table.insert().values(user_id=user_id, prompt=prompt, url=url))
    await session.commit()
    return url




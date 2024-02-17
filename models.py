import sqlalchemy


metadata = sqlalchemy.MetaData()


dalle_image_table = sqlalchemy.Table(
    "dalle_image",
    metadata,
    sqlalchemy.Column("user_id", sqlalchemy.BigInteger, primary_key=True),
    sqlalchemy.Column("prompt", sqlalchemy.Text),
    sqlalchemy.Column("url", sqlalchemy.Text),
)

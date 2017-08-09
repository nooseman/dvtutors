from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
users = Table('users', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('social_id', String(length=64), nullable=False),
    Column('nickname', String(length=64), nullable=False),
    Column('email', String(length=64)),
    Column('about_me', String(length=256)),
    Column('profile_picture_url', String(length=64)),
    Column('last_room_password', String(length=64)),
    Column('auth_provider', String(length=64), nullable=False),
    Column('total_time_online', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['users'].columns['last_room_password'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['users'].columns['last_room_password'].drop()

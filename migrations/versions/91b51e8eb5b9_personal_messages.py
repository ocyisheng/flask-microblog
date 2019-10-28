"""personal messages

Revision ID: 91b51e8eb5b9
Revises: 43ea84827bd0
Create Date: 2019-09-02 11:40:14.458580

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91b51e8eb5b9'
down_revision = '43ea84827bd0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('recipient_id', sa.Integer(), nullable=True),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.ForeignKeyConstraint(['recipient_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('user', sa.Column('last_message_read_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_message_read_time')
    op.drop_table('message')
    # ### end Alembic commands ###
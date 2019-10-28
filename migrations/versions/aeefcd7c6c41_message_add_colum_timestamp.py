"""Message add colum timestamp

Revision ID: aeefcd7c6c41
Revises: 91b51e8eb5b9
Create Date: 2019-09-02 20:38:16.669246

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aeefcd7c6c41'
down_revision = '91b51e8eb5b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('timestamp', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_message_timestamp'), 'message', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_message_timestamp'), table_name='message')
    op.drop_column('message', 'timestamp')
    # ### end Alembic commands ###
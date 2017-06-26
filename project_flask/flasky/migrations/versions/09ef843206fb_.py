"""empty message

Revision ID: 09ef843206fb
Revises: 
Create Date: 2017-06-25 22:39:15.217376

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09ef843206fb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('proposal')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('proposal',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_proposed_to', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('request_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['request_id'], ['request.id'], name='proposal_request_id_fkey'),
    sa.ForeignKeyConstraint(['user_proposed_to'], ['user.id'], name='proposal_user_proposed_to_fkey'),
    sa.PrimaryKeyConstraint('id', name='proposal_pkey')
    )
    # ### end Alembic commands ###

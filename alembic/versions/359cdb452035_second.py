"""second

Revision ID: 359cdb452035
Revises: 7f23435664a6
Create Date: 2021-12-03 12:55:37.789211

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '359cdb452035'
down_revision = '7f23435664a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Student',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('student_first_name', sa.String(length=45), nullable=False),
    sa.Column('student_last_name', sa.String(length=45), nullable=False),
    sa.Column('student_average_grade', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('student_age', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('User',
    sa.Column('username', sa.String(length=45), nullable=False),
    sa.Column('first_name', sa.String(length=45), nullable=False),
    sa.Column('last_name', sa.String(length=45), nullable=False),
    sa.Column('email', sa.String(length=45), nullable=False),
    sa.Column('phone', sa.String(length=45), nullable=True),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('username'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone'),
    sa.UniqueConstraint('username')
    )
    op.create_table('Rank',
    sa.Column('rank_id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('last_change', sa.TIMESTAMP(), nullable=False),
    sa.Column('changed_by', sa.String(length=45), nullable=False),
    sa.ForeignKeyConstraint(['changed_by'], ['User.username'], ),
    sa.ForeignKeyConstraint(['student_id'], ['Student.id'], ),
    sa.PrimaryKeyConstraint('rank_id'),
    sa.UniqueConstraint('rank_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Rank')
    op.drop_table('User')
    op.drop_table('Student')
    # ### end Alembic commands ###

"""initial commit

Revision ID: 192ef9ee151d
Revises: 
Create Date: 2023-12-04 22:24:00.857372

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '192ef9ee151d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('interviewers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('inn', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.LargeBinary(), nullable=False),
    sa.Column('organization_name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('respondents_base_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('family_status', sa.Enum('single', 'married', name='familystatus'), nullable=True),
    sa.Column('children', sa.Boolean(), nullable=True),
    sa.Column('income', sa.Enum('UP_TO_10000', 'FROM_10001_TO_30000', 'FROM_30001_TO_50000', 'FROM_50001_TO_70000', 'FROM_70001_TO_90000', 'FROM_90001_TO_110000', 'OVER_110000', 'NO_INCOME', name='incomestatus'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('respondents_education_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('education_status', sa.Enum('WITHOUT_EDUCATION', 'INCOMPLETE_SECONDARY', 'SECONDARY', 'SPECIAL_SECONDARY', 'INCOMPLETE_HIGHER', 'HIGHER', 'TWO_OR_MORE_HIGHER', 'ACADEMIC_DEGREE', name='educationstatuses'), nullable=True),
    sa.Column('work_status', sa.Enum('EDUCATION', 'COMMERCIAL_EMPLOYMENT', 'OWN_BUSINESS', 'MILITARY_SERVICE', 'GOVERNMENT_EMPLOYMENT', 'MATERNITY_LEAVE', 'HOUSEHOLD_MANAGEMENT', 'RETIRED', 'UNEMPLOYED', 'CLERGY', 'FREELANCE', 'OTHER', name='workstatuses'), nullable=True),
    sa.Column('language', sa.Enum('ENGLISH', 'ITALIAN', 'SPANISH', 'CHINESE', 'GERMAN', 'RUSSIAN', 'UKRAINIAN', 'FRENCH', 'JAPANESE', 'OTHER', name='languages'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('respondents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('surname', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.LargeBinary(), nullable=False),
    sa.Column('gender', sa.String(), nullable=False),
    sa.Column('country', sa.String(), nullable=False),
    sa.Column('city', sa.String(), nullable=False),
    sa.Column('base_info_id', sa.Integer(), nullable=True),
    sa.Column('education_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['base_info_id'], ['respondents_base_info.id'], ),
    sa.ForeignKeyConstraint(['education_id'], ['respondents_education_info.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('surveys',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('end_date', sa.Date(), nullable=False),
    sa.Column('interviewers_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.Enum('active', 'inactive', name='surveystatus'), nullable=True),
    sa.ForeignKeyConstraint(['interviewers_id'], ['interviewers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('surveys')
    op.drop_table('respondents')
    op.drop_table('respondents_education_info')
    op.drop_table('respondents_base_info')
    op.drop_table('interviewers')
    # ### end Alembic commands ###

"""Create calendar_hours materialized view

Revision ID: fe8f12ced31a
Revises: 864bb00bc205
Create Date: 2025-10-28 11:45:33.154967+00:00

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "fe8f12ced31a"
down_revision: Union[str, None] = "864bb00bc205"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Materialized View anlegen
    op.execute(
        """
    CREATE MATERIALIZED VIEW calendar_hours AS
    SELECT generate_series(
      '2019-10-09 23:59:00'::timestamptz,
      date_trunc('day', now() + interval '1 day') + interval '23:59:00',
      '1 hour'
    ) AS collected_at
    WITH NO DATA;
    """
    )

    # 2. Index auf collected_at
    op.execute(
        """
    CREATE UNIQUE INDEX ix_calendar_hours_collected_at
      ON calendar_hours(collected_at);
    """
    )

    # 3. Sofortiges einmaliges Befüllen
    op.execute("REFRESH MATERIALIZED VIEW calendar_hours;")


def downgrade() -> None:
    op.execute("DROP MATERIALIZED VIEW IF EXISTS calendar_hours;")

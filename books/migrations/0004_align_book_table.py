from django.db import migrations, models


def ensure_books_table(apps, schema_editor):
    connection = schema_editor.connection
    existing_tables = connection.introspection.table_names()

    # Preserve the existing table and its records.
    if "books" in existing_tables:
        return

    # Create the table only when it does not exist.
    qn = schema_editor.quote_name

    schema_editor.execute(
        f"""
        CREATE TABLE {qn('books')} (
            {qn('book_id')} varchar(20) PRIMARY KEY,
            {qn('title')} varchar(200) NOT NULL,
            {qn('author')} varchar(100) NOT NULL,
            {qn('available')} boolean NULL
        )
        """
    )


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_alter_book_options'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunPython(
                    ensure_books_table,
                    migrations.RunPython.noop,
                ),
            ],
            state_operations=[
                migrations.RemoveField(
                    model_name='book',
                    name='id',
                ),
                migrations.AddField(
                    model_name='book',
                    name='book_id',
                    field=models.CharField(
                        max_length=20,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                migrations.AlterModelTable(
                    name='book',
                    table='books',
                ),
            ],
        ),
    ]
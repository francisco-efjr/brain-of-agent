class CustomerNotFound(LookupError):
    """Identical public error for absent and inaccessible customers."""

def edit_customer(db, authenticated_tenant, customer_id, name):
    if not isinstance(name, str):
        raise ValueError('name must be nonempty text of at most 100 characters')
    normalized = name.strip()
    if not normalized or len(normalized) > 100:
        raise ValueError('name must be nonempty text of at most 100 characters')
    with db:
        cursor = db.execute('UPDATE customers SET name = ? WHERE id = ? AND tenant_id = ?', (normalized, customer_id, authenticated_tenant))
        if cursor.rowcount != 1:
            raise CustomerNotFound('Customer not found')

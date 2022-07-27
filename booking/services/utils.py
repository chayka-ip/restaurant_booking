def try_get_int(n):
    """ Returns integer if n can be cast to it; eiter: -1 """
    try:
        return int(n)
    except Exception:
        return -1


def generate_customer_cancel_booking_link(request, cancel_id: str):
    from booking.urls import get_customer_discard_booking_api
    customer_discard_api = get_customer_discard_booking_api(request=request)
    return customer_discard_api + f'?id={cancel_id}'

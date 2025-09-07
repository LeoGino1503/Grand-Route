def is_near(obj1, obj2, distance=80):
    """Kiểm tra khoảng cách giữa 2 object"""
    dx = obj1.x - obj2.x
    dy = obj1.y - obj2.y
    return (dx * dx + dy * dy) ** 0.5 < distance

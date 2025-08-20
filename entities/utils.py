def scale_value(start_val, lvl, val_k=1.1):
    """Улучшение параметров на lvl (1.1^lvl по умолчанию)"""
    return round(start_val * (val_k ** lvl))


def upgrade_cost(start_cost, lvl, cost_k=1.3):
    """Стоимость улучшения для lvl (1.3^lvl по умолчанию)"""
    return round(start_cost * (cost_k ** lvl))

GEO_RADIUS = 'Geo Radius'
MAPPING = 'Mapping'
TIME_RADIUS = 'Time Radius'

LOCATION_RANGE_TYPE_OPTION = (
    (GEO_RADIUS, GEO_RADIUS),
    (MAPPING, MAPPING),
    (TIME_RADIUS, TIME_RADIUS)
)

STAND_ALONE = 'Stand Alone'
PARENT_PRODUCT = 'Parent Product'
CHILD_PRODUCT = 'Child Product'

PRODUCT_STRUCTURE_OPTION = (
    (STAND_ALONE, STAND_ALONE),
    (PARENT_PRODUCT, PARENT_PRODUCT),
    (CHILD_PRODUCT, CHILD_PRODUCT)
)

DRY = 'Dry'
FROZEN = 'Frozen'
CHILLED = 'Chilled'

PRODUCT_STATE_OPTION = (
    (DRY, DRY),
    (FROZEN, FROZEN),
    (CHILLED, CHILLED),
)

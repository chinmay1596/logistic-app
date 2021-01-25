from import_export import resources
from.models import OrderItem
 
class PersonResource(resources.ModelResource):
	class meta:
		model=OrderItem
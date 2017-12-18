"""
    Common views
"""

from core_curate_app.views.user.views import _get_curate_data_structure_by_id, render_xml
from core_main_app.views.common.views import CommonView


class FormView(CommonView):
    """
        Form View
    """

    def get(self, request, *args, **kwargs):
        try:
            # get data structure
            curate_data_structure = _get_curate_data_structure_by_id(kwargs['curate_data_structure_id'], request)

            # TODO: fix with the rework on the curate workflow
            if curate_data_structure.form_string is None:
                raise Exception("The form was not saved. We can't display the correct data.")

            # Set the assets
            assets = {
                "js": [
                    {
                        "path": "core_main_app/common/js/XMLTree.js",
                        "is_raw": False
                    },
                    {
                        "path": 'core_main_app/user/js/data/detail.js',
                        "is_raw": False
                    }
                ],
                "css": ['core_main_app/common/css/XMLTree.css']
            }

            # Set the context
            context = {
                "data_structure": curate_data_structure,
            }

            return self.common_render(request,
                                      'core_curate_app/user/detail.html',
                                      assets=assets,
                                      context=context)
        except Exception, e:
            return self.common_render(request,
                                      'core_curate_app/user/errors.html',
                                      assets={},
                                      context={'errors': e.message})

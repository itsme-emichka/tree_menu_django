from django.template import Library
from django.template.context import RequestContext
from django.db.models.query import QuerySet

from menu.models import Section


register = Library()


def create_layer(
        current_layer_sections: list[Section],
        current_section: Section,
        current_children: dict[str: Section, str: list]
        ) -> list[Section, list[Section, list]]:
    layer = []
    for current_layer_section in current_layer_sections:
        if current_layer_section == current_section:
            layer.append(
                {
                    'section': current_layer_section,
                    'section_children': current_children
                }
            )
        else:
            layer.append(
                {
                    'section': current_layer_section
                }
            )
    return layer


def menu_generator(
        all_sections: QuerySet,
        current_section: Section,
        current_children: dict[str: Section, str: list],
        parent_sections: list[Section],
        ) -> list[Section, list[Section, list]]:
    parent = current_section.parent
    if not parent:
        return create_layer(
            parent_sections, current_section, current_children)

    menu_layer = create_layer(
        current_layer_sections=all_sections.filter(parent=parent),
        current_section=current_section,
        current_children=current_children
    )
    return menu_generator(all_sections, parent, menu_layer, parent_sections)


@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context: RequestContext, menu_name: str) -> str:
    current_url = context.request.path
    all_sections = Section.objects.filter(menu__title=menu_name)
    parent_sections = [section for section in all_sections.filter(parent=None)]
    current_section = all_sections.get(url__endswith=current_url)
    current_children = [
        {
            'section': section
        } for section in all_sections.filter(parent=current_section)
    ]

    sections = menu_generator(
        all_sections=all_sections,
        current_section=current_section,
        current_children=current_children,
        parent_sections=parent_sections
    )

    final = {'sections': sections}
    return final

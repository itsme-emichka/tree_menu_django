from django.template import Library
from django.template.context import RequestContext
from django.db.models.query import QuerySet

from menu.models import Section


register = Library()


def create_layer(
        current_layer_sections: list[Section],
        current_section: Section,
        current_children: list[dict[str: Section, str: list]]
        ) -> list[dict[str: Section, str: list]]:
    layer = []
    for current_layer_section in current_layer_sections:
        if current_layer_section == current_section:
            layer.append({
                'section': current_layer_section,
                'section_children': current_children})
        else:
            layer.append({'section': current_layer_section})
    return layer


def get_section(section_id, all_sections) -> Section:
    for section in all_sections:
        if section.id == section_id:
            return section


def menu_generator(
        all_sections: QuerySet,
        current_section: Section,
        current_children: dict[str: Section, str: list],
        parent_sections: list[Section],
        children_of_sections: dict[Section, list[Section]]
        ) -> list[dict[str: Section, str: list]]:
    parent_id = current_section.parent_id
    if not parent_id:
        return create_layer(
            parent_sections, current_section, current_children)

    menu_layer = create_layer(
        current_layer_sections=children_of_sections.get(parent_id, []),
        current_section=current_section,
        current_children=current_children
    )
    return menu_generator(
        all_sections=all_sections,
        current_section=get_section(parent_id, all_sections),
        current_children=menu_layer,
        parent_sections=parent_sections,
        children_of_sections=children_of_sections
    )


@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context: RequestContext, menu_name: str) -> str:
    all_sections = Section.objects.filter(menu__title=menu_name)

    parent_sections = []
    children_of_sections = {}
    current_section = None

    for section in all_sections:
        if section.url == context.request.build_absolute_uri():
            current_section = section
        if not section.parent_id:
            parent_sections.append(section)
        else:
            if children_of_sections.get(section.parent_id, None):
                children_of_sections[section.parent_id].append(section)
            else:
                children_of_sections[section.parent_id] = [section]

    if not current_section:
        return {
            'sections': [{'section': section} for section in parent_sections]}

    current_children = [{
            'section': section
        } for section in children_of_sections.get(current_section.id, [])]

    sections = menu_generator(
        all_sections=all_sections,
        current_section=current_section,
        current_children=current_children,
        parent_sections=parent_sections,
        children_of_sections=children_of_sections
    )
    return {'sections': sections}

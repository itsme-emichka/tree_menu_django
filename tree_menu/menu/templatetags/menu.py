from django.template import Library
from django.template.context import RequestContext

from menu.models import Section


register = Library()


def create_layer(
        current_layer_sections: list[Section],
        current_section: Section,
        current_children: list[dict[str: Section, str: list]]
        ) -> list[dict[str: Section, str: list]]:
    '''Формирует слой вложенных разделов меню.'''
    layer = []
    for current_layer_section in current_layer_sections:
        if current_layer_section == current_section:
            layer.append({
                'section': current_layer_section,
                'section_children': current_children})
        else:
            layer.append({'section': current_layer_section})
    return layer


def menu_generator(
        all_sections: dict[int, Section],
        current_section: Section,
        parent_sections: list[Section],
        children_of_sections: dict[Section, list[Section]]
        ) -> list[dict[str: Section, str: list]]:
    '''Генерирует меню.'''

    def generate_menu(
            current_section: Section,
            current_children: list[dict[str: Section, str: list]]
            ) -> list[dict[str: Section, str: list]]:
        '''Рекурсивно собирает меню по слоям.'''
        parent_id = current_section.parent_id

        if not parent_id:
            return create_layer(
                parent_sections, current_section, current_children)

        menu_layer = create_layer(
            current_layer_sections=children_of_sections.get(parent_id, []),
            current_section=current_section,
            current_children=current_children
        )
        return generate_menu(all_sections.get(parent_id, None), menu_layer)

    return generate_menu(
        current_section,
        [{'section': section}
         for section in children_of_sections.get(current_section.id, [])]
    )


@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context: RequestContext, menu_name: str) -> str:
    '''Template tag для размещения древовидного меню в html шаблонах.'''
    all_sections = Section.objects.filter(menu__title=menu_name)

    parent_sections = []
    children_of_sections = {}
    current_section = None
    sections_with_id = dict()

    for section in all_sections:
        sections_with_id[section.id] = section
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

    return {'sections': menu_generator(
        all_sections=sections_with_id,
        current_section=current_section,
        parent_sections=parent_sections,
        children_of_sections=children_of_sections
    )}

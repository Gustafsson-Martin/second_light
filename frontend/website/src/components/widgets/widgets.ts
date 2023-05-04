/* 
Update this file when new widgets are added.
Widgets should not be imported in any other file.

TODO: Check that widgets imported follow some widget interface.
*/

import TodoListWidget from "./todolist/TodoListWidget.vue";
import ClockWidget from "./clock/ClockWidget.vue";
import SearchWidget from "./search/SearchWidget.vue";
import NoteWidget from "./note/NoteWidget.vue";
import BookmarksWidget from "./bookmarks/BookmarksWidget.vue";

export const widgetTypes = {
    TodoListWidget,
    ClockWidget,
    SearchWidget,
    NoteWidget,
    BookmarksWidget,
};

export const widgetKeys: (keyof typeof widgetTypes)[] = Object.keys(widgetTypes) as (keyof typeof widgetTypes)[];

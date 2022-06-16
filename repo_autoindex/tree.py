from dataclasses import dataclass, field, replace

from .base import IndexEntry, ICON_FOLDER


@dataclass
class TreeNode:
    entries: list[IndexEntry] = field(default_factory=list)
    children: list["TreeNode"] = field(default_factory=list)
    relative_dir: str = ""


def treeify(
    all_entries: list[IndexEntry], relative_dir: str = "", index_href_suffix: str = ""
) -> TreeNode:
    out = TreeNode(relative_dir=relative_dir)

    if relative_dir:
        out.entries.append(
            IndexEntry(
                icon=ICON_FOLDER,
                href=f"../{index_href_suffix}",
                text="parent directory",
            )
        )

    entries_by_leading_dir = {}
    for entry in all_entries:
        subdir = entry.href.removeprefix(relative_dir + "/")
        components = subdir.split("/", 1)
        if len(components) == 1:
            # file is in this dir
            subdir = ""
        else:
            subdir = components[0]
        entries_by_leading_dir.setdefault(subdir, []).append(entry)

    for key in sorted(entries_by_leading_dir.keys()):
        if key:
            out.entries.append(
                IndexEntry(
                    icon=ICON_FOLDER,
                    href=f"{key}/{index_href_suffix}",
                    text=f"{key}/",
                    # TODO: in theory we could look up the latest time and sum
                    # the sizes here.
                    time=" ",
                    size=" ",
                )
            )
            sub_entries = entries_by_leading_dir[key]
            subdir = key
            if relative_dir:
                subdir = f"{relative_dir}/{subdir}"
            out.children.append(
                treeify(
                    sub_entries,
                    relative_dir=subdir,
                    index_href_suffix=index_href_suffix,
                )
            )
        else:
            out.entries.extend(
                [
                    replace(e, href=e.href.removeprefix(relative_dir + "/"))
                    for e in entries_by_leading_dir[key]
                ]
            )

    return out

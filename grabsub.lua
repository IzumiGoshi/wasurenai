require "mp"


ANIME_LINES = "/home/goshi/.config/mpv/anime_lines.txt"
sep = "<====>"
line_sep = "[====]"


function append_to_file(fname, text)
    io.output(io.open(fname, "a"))
    io.write(text)
    io.close()
end

function save_sub()
    curt = mp.get_property("time-pos")
    start = tostring(mp.get_property("sub-start"))
    endt = tostring(mp.get_property("sub-end"))
    subtitle = mp.get_property("sub-text")
    animefile = mp.get_property("path")
    tracks = mp.get_property("track-list")

    subtitle = string.gsub(subtitle, "\n", "<br>")
    line_output = subtitle..sep..animefile..sep..curt..sep..start..sep..endt..line_sep.."\n"
    append_to_file(ANIME_LINES, line_output)
    mp.osd_message("writing line...", 1)
end


mp.add_key_binding("b", "save_sub", save_sub)

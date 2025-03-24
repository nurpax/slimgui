
local api_html = nil
local imgui_version = nil

local func_dict = {}
local class_dict = {}

function add_func(name, code)
    local prev = func_dict[name]
    if prev then
        table.insert(prev, code)
    else
        func_dict[name] = { code }
    end
end

function load_api_html()
    local fh = io.open(api_html)
    local str = fh:read('*all')
    fh:close()
    local code = ""
    local in_state = nil
    local sym_name = nil
    for line in str:gmatch("[^\r\n]+") do
        if in_state == nil then
            local tmp_func = line:match("%$%$func=([%w_]+)")
            local tmp_class = line:match("%$%$class=([%w_]+)")
            if tmp_func then
                in_state = "func"
                sym_name = tmp_func
            elseif tmp_class then
                in_state = "class"
                sym_name = tmp_class
            end
        elseif in_state == "class" then
            if line:match("%$%$end") then
                in_state = nil
                class_dict[sym_name] = code
                code = ""
            else
                code = code .. line .. "\n"
            end
        elseif in_state == "func" then
            if line:match("%$%$end") then
                in_state = nil
                add_func(sym_name, code)
                code = ""
            else
                code = code .. line .. "\n"
            end
        end
    end
end

function get_vars (meta)
    for k, v in pairs(meta) do
        if k == 'api_html' then
            api_html = v
        elseif k == 'imgui_version' then
            imgui_version = v
        end
    end
    load_api_html()
end

-- Replace divs with 'raw-html-insert' class in them with raw HTML from a file
function div (el)
    local funcrefs = el.attributes['data-apirefs']
    local out_html = ""
    for func in string.gmatch(funcrefs, '([^,]+)') do
        name = func:match("^%s*(.-)%s*$") -- strip ws
        if func_dict[name] then
            for _, code in ipairs(func_dict[name]) do
                out_html = out_html .. code
            end
        elseif class_dict[name] then
            out_html = out_html .. class_dict[name]
        else
            print("[WARN] No function found for " .. name)
        end
    end
    return {
        pandoc.RawBlock('html', out_html)
    }
end

-- a pandoc filter that replace $imgui_version$ with the actual metadata value
function replace_metadata(elem)
    if elem.text and elem.text == "%imguiversion%." then
        return pandoc.Str(imgui_version .. ".")
    elseif elem.text and elem.text == "%imguiversion%" then
        return pandoc.Str(imgui_version)
    end
    return elem
end

return {{Meta = get_vars}, {Div = div}, {Str = replace_metadata}}

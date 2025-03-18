
local api_html = nil
local func_dict = {}
local class_dict = {}

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
                in_state = "class"
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
                func_dict[sym_name] = code
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
            out_html = out_html .. func_dict[name]
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

return {{Meta = get_vars}, {Div = div}}

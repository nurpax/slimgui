
local api_html = nil
local func_dict = {}

function load_api_html()
    local fh = io.open(api_html)
    local str = fh:read('*all')
    fh:close()
    local func_code = ""
    local in_func = false
    local func_name = nil
    for line in str:gmatch("[^\r\n]+") do
        if not in_func then
            func_name = line:match("%$%$func=([%w_]+)")
            if func_name then
                in_func = true
            end
        else
            if line:match("%$%$end") then
                in_func = false
                func_dict[func_name] = func_code
                func_code = ""
            else
                func_code = func_code .. line .. "\n"
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
    local func_html = ""
    for func in string.gmatch(funcrefs, '([^,]+)') do
        func = func:match("^%s*(.-)%s*$") -- strip ws

        if func_dict[func] then
            func_html = func_html .. func_dict[func]
        else
            print("[WARN] No function found for " .. func)
        end
    end
    return {
        pandoc.RawBlock('html', func_html)
    }
end

return {{Meta = get_vars}, {Div = div}}

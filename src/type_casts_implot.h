template <> struct nanobind::detail::type_caster<ImPlotPoint> {
    using Value = ImPlotPoint;
    using Caster = make_caster<double>;
    template <typename T> using Cast = Value;

    // Value name for docstring generation
    static constexpr auto Name = const_name(NB_TYPING_TUPLE "[") + concat(Caster::Name, Caster::Name) + const_name("]");

    template <typename T_> static constexpr bool can_cast() { return true; }

    bool from_python(handle src, uint8_t flags, cleanup_list *cleanup) noexcept {
        PyObject *temp; // always initialized by the following line
        PyObject **o = seq_get_with_size(src.ptr(), 2, &temp);
        bool success = o &&
                       caster1.from_python(o[0], flags, cleanup) &&
                       caster2.from_python(o[1], flags, cleanup);
        Py_XDECREF(temp);
        return success;
    }

    template <typename T>
    static handle from_cpp(T *value, rv_policy policy, cleanup_list *cleanup) {
        if (!value)
            return none().release();
        return from_cpp(*value, policy, cleanup);
    }

    template <typename T>
    static handle from_cpp(T &&value, rv_policy policy, cleanup_list *cleanup) noexcept {
        object o1 = steal(Caster::from_cpp(forward_like_<T>(value.x), policy, cleanup));
        if (!o1.is_valid())
            return {};
        object o2 = steal(Caster::from_cpp(forward_like_<T>(value.y), policy, cleanup));
        if (!o2.is_valid())
            return {};
        PyObject *r = PyTuple_New(2);
        NB_TUPLE_SET_ITEM(r, 0, o1.release().ptr());
        NB_TUPLE_SET_ITEM(r, 1, o2.release().ptr());
        return r;
    }

    explicit operator Value() {
        return Value(caster1.operator cast_t<double>(), caster2.operator cast_t<double>());
    }
    Caster caster1;
    Caster caster2;
};

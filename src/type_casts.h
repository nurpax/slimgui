
#pragma once

struct Vec3 {
    float x, y, z;
    constexpr Vec3() : x(0.0f), y(0.0f), z(0.0f) { }
    constexpr Vec3(float _x, float _y, float _z)    : x(_x), y(_y), z(_z) { }
};

template <> struct nanobind::detail::type_caster<ImVec2> {
    using Value = ImVec2;
    using Caster = make_caster<float>;
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
        return Value(caster1.operator cast_t<float>(), caster2.operator cast_t<float>());
    }
    Caster caster1;
    Caster caster2;
};

template <> struct nanobind::detail::type_caster<Vec3> {
    using Value = Vec3;
    using Caster = make_caster<float>;
    template <typename T> using Cast = Value;

    // Value name for docstring generation
    static constexpr auto Name =
        const_name(NB_TYPING_TUPLE "[") + concat(Caster::Name, Caster::Name, Caster::Name) + const_name("]");

    bool from_python(handle src, uint8_t flags,
                     cleanup_list *cleanup) noexcept {
        PyObject *temp; // always initialized by the following line
        PyObject **o = seq_get_with_size(src.ptr(), 3, &temp);
        bool success = o &&
                       caster1.from_python(o[0], flags, cleanup) &&
                       caster2.from_python(o[1], flags, cleanup) &&
                       caster3.from_python(o[2], flags, cleanup);
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
    static handle from_cpp(T &&value, rv_policy policy,
                           cleanup_list *cleanup) noexcept {
        object o1 = steal(Caster::from_cpp(forward_like_<T>(value.x), policy, cleanup));
        object o2 = steal(Caster::from_cpp(forward_like_<T>(value.y), policy, cleanup));
        object o3 = steal(Caster::from_cpp(forward_like_<T>(value.z), policy, cleanup));
        if (!o1.is_valid() || !o2.is_valid() || !o3.is_valid())
            return {};
        PyObject *r = PyTuple_New(3);
        NB_TUPLE_SET_ITEM(r, 0, o1.release().ptr());
        NB_TUPLE_SET_ITEM(r, 1, o2.release().ptr());
        NB_TUPLE_SET_ITEM(r, 2, o3.release().ptr());
        return r;
    }

    explicit operator Value() {
        return Value(caster1.operator cast_t<float>(),
                     caster2.operator cast_t<float>(),
                     caster3.operator cast_t<float>());
    }

    Caster caster1, caster2, caster3;
};

template <> struct nanobind::detail::type_caster<ImVec4> {
    using Value = ImVec4;
    using Caster = make_caster<float>;
    template <typename T> using Cast = Value;

    // Value name for docstring generation
    static constexpr auto Name =
        const_name(NB_TYPING_TUPLE "[") + concat(Caster::Name, Caster::Name, Caster::Name, Caster::Name) + const_name("]");

    template <typename T_> static constexpr bool can_cast() { return true; }

    bool from_python(handle src, uint8_t flags,
                     cleanup_list *cleanup) noexcept {
        PyObject *temp; // always initialized by the following line
        PyObject **o = seq_get_with_size(src.ptr(), 4, &temp);
        bool success = o &&
                       caster1.from_python(o[0], flags, cleanup) &&
                       caster2.from_python(o[1], flags, cleanup) &&
                       caster3.from_python(o[2], flags, cleanup) &&
                       caster4.from_python(o[3], flags, cleanup);
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
    static handle from_cpp(T &&value, rv_policy policy,
                           cleanup_list *cleanup) noexcept {
        object o1 = steal(Caster::from_cpp(forward_like_<T>(value.x), policy, cleanup));
        object o2 = steal(Caster::from_cpp(forward_like_<T>(value.y), policy, cleanup));
        object o3 = steal(Caster::from_cpp(forward_like_<T>(value.z), policy, cleanup));
        object o4 = steal(Caster::from_cpp(forward_like_<T>(value.w), policy, cleanup));
        if (!o1.is_valid() || !o2.is_valid() || !o3.is_valid() || !o4.is_valid())
            return {};
        PyObject *r = PyTuple_New(4);
        NB_TUPLE_SET_ITEM(r, 0, o1.release().ptr());
        NB_TUPLE_SET_ITEM(r, 1, o2.release().ptr());
        NB_TUPLE_SET_ITEM(r, 2, o3.release().ptr());
        NB_TUPLE_SET_ITEM(r, 3, o4.release().ptr());
        return r;
    }

    explicit operator Value() {
        return Value(caster1.operator cast_t<float>(),
                     caster2.operator cast_t<float>(),
                     caster3.operator cast_t<float>(),
                     caster4.operator cast_t<float>());
    }

    Caster caster1, caster2, caster3, caster4;
};


(globalThis.TURBOPACK = globalThis.TURBOPACK || []).push(["static/chunks/_50ea1f._.js", {

"[project]/lib/constant.ts [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { r: __turbopack_require__, f: __turbopack_module_context__, i: __turbopack_import__, s: __turbopack_esm__, v: __turbopack_export_value__, n: __turbopack_export_namespace__, c: __turbopack_cache__, M: __turbopack_modules__, l: __turbopack_load__, j: __turbopack_dynamic__, P: __turbopack_resolve_absolute_path__, U: __turbopack_relative_url__, R: __turbopack_resolve_module_id_path__, b: __turbopack_worker_blob_url__, g: global, __dirname, k: __turbopack_refresh__, m: module, z: __turbopack_require_stub__ } = __turbopack_context__;
{
__turbopack_esm__({
    "ACCESS_TOKEN": (()=>ACCESS_TOKEN),
    "REFRESH_TOKEN": (()=>REFRESH_TOKEN)
});
const ACCESS_TOKEN = 'access';
const REFRESH_TOKEN = 'refresh';
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_refresh__.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
"[project]/lib/api.ts [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { r: __turbopack_require__, f: __turbopack_module_context__, i: __turbopack_import__, s: __turbopack_esm__, v: __turbopack_export_value__, n: __turbopack_export_namespace__, c: __turbopack_cache__, M: __turbopack_modules__, l: __turbopack_load__, j: __turbopack_dynamic__, P: __turbopack_resolve_absolute_path__, U: __turbopack_relative_url__, R: __turbopack_resolve_module_id_path__, b: __turbopack_worker_blob_url__, g: global, __dirname, k: __turbopack_refresh__, m: module, z: __turbopack_require_stub__ } = __turbopack_context__;
{
__turbopack_esm__({
    "default": (()=>__TURBOPACK__default__export__)
});
var __TURBOPACK__imported__module__$5b$project$5d2f$lib$2f$constant$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_import__("[project]/lib/constant.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_import__("[project]/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$axios$2f$lib$2f$axios$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_import__("[project]/node_modules/axios/lib/axios.js [app-client] (ecmascript)");
;
;
const BASE_URL = ("TURBOPACK compile-time value", "http://127.0.0.1:8000");
const api = __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$axios$2f$lib$2f$axios$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].create({
    baseURL: BASE_URL,
    headers: {
        "Content-Type": "application/json"
    }
});
api.interceptors.request.use((config)=>{
    if ("TURBOPACK compile-time truthy", 1) {
        const token = localStorage.getItem(__TURBOPACK__imported__module__$5b$project$5d2f$lib$2f$constant$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["ACCESS_TOKEN"]);
        if (token) {
            config.headers = config.headers || {};
            config.headers.Authorization = `Bearer ${token}`;
        }
    }
    return config;
}, (error)=>Promise.reject(error));
const AUTH_ENDPOINTS = [
    "/auth/token/",
    "/auth/user/"
];
api.interceptors.response.use((response)=>response, async (error)=>{
    const originalRequest = error.config;
    if (!originalRequest || originalRequest.url === undefined) {
        return Promise.reject(error);
    }
    const isAuthEndpoint = AUTH_ENDPOINTS.some((endpoint)=>originalRequest.url?.startsWith(endpoint) || originalRequest.url === endpoint);
    if (isAuthEndpoint) {
        return Promise.reject(error);
    }
    if (error.response?.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;
        if ("TURBOPACK compile-time truthy", 1) {
            const refreshToken = localStorage.getItem(__TURBOPACK__imported__module__$5b$project$5d2f$lib$2f$constant$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["REFRESH_TOKEN"]);
            if (refreshToken) {
                try {
                    const res = await api.post("/auth/token/refresh/", {
                        refresh: refreshToken
                    });
                    if (res.status === 200 && res.data?.access) {
                        const newAccessToken = res.data.access;
                        localStorage.setItem(__TURBOPACK__imported__module__$5b$project$5d2f$lib$2f$constant$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["ACCESS_TOKEN"], newAccessToken);
                        originalRequest.headers = originalRequest.headers || {};
                        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
                        return api(originalRequest);
                    }
                } catch (refreshError) {
                    localStorage.removeItem(__TURBOPACK__imported__module__$5b$project$5d2f$lib$2f$constant$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["ACCESS_TOKEN"]);
                    localStorage.removeItem(__TURBOPACK__imported__module__$5b$project$5d2f$lib$2f$constant$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["REFRESH_TOKEN"]);
                    if ("TURBOPACK compile-time truthy", 1) {
                        window.location.href = "/login";
                    }
                }
            } else {
                if ("TURBOPACK compile-time truthy", 1) {
                    window.location.href = "/login";
                }
            }
        }
    }
    return Promise.reject(error);
});
const __TURBOPACK__default__export__ = api;
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_refresh__.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
"[project]/components/ProtectedRoute.tsx [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { r: __turbopack_require__, f: __turbopack_module_context__, i: __turbopack_import__, s: __turbopack_esm__, v: __turbopack_export_value__, n: __turbopack_export_namespace__, c: __turbopack_cache__, M: __turbopack_modules__, l: __turbopack_load__, j: __turbopack_dynamic__, P: __turbopack_resolve_absolute_path__, U: __turbopack_relative_url__, R: __turbopack_resolve_module_id_path__, b: __turbopack_worker_blob_url__, g: global, __dirname, k: __turbopack_refresh__, m: module, z: __turbopack_require_stub__ } = __turbopack_context__;
{
__turbopack_esm__({
    "default": (()=>__TURBOPACK__default__export__)
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_import__("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_import__("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$navigation$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_import__("[project]/node_modules/next/navigation.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$lib$2f$constant$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_import__("[project]/lib/constant.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$jwt$2d$decode$2f$build$2f$esm$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_import__("[project]/node_modules/jwt-decode/build/esm/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$lib$2f$api$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_import__("[project]/lib/api.ts [app-client] (ecmascript)");
;
var _s = __turbopack_refresh__.signature();
"use client";
;
;
;
;
;
const ProtectedRoute = ({ children })=>{
    _s();
    const [isAuthorized, setIsAuthorized] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(null);
    const [isLoading, setIsLoading] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(true);
    const router = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$navigation$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useRouter"])();
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "ProtectedRoute.useEffect": ()=>{
            if ("TURBOPACK compile-time falsy", 0) {
                "TURBOPACK unreachable";
            }
            const checkAuth = {
                "ProtectedRoute.useEffect.checkAuth": async ()=>{
                    try {
                        await auth();
                    } catch (error) {
                        setIsAuthorized(false);
                        setIsLoading(false);
                    }
                }
            }["ProtectedRoute.useEffect.checkAuth"];
            checkAuth();
        }
    }["ProtectedRoute.useEffect"], []);
    const refresh = async ()=>{
        const refreshToken = localStorage.getItem(__TURBOPACK__imported__module__$5b$project$5d2f$lib$2f$constant$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["REFRESH_TOKEN"]);
        try {
            const res = await __TURBOPACK__imported__module__$5b$project$5d2f$lib$2f$api$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].post("auth/token/refresh", {
                refresh: refreshToken
            });
            if (res.status === 200) {
                setIsAuthorized(true);
                localStorage.setItem(__TURBOPACK__imported__module__$5b$project$5d2f$lib$2f$constant$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["ACCESS_TOKEN"], res.data.access);
            } else {
                setIsAuthorized(false);
            }
        } catch (error) {
            console.log("Error in Refreshing Token", error);
            setIsAuthorized(false);
        }
        setIsLoading(false);
    };
    const auth = async ()=>{
        const token = localStorage.getItem(__TURBOPACK__imported__module__$5b$project$5d2f$lib$2f$constant$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["ACCESS_TOKEN"]);
        if (!token) {
            setIsAuthorized(false);
            setIsLoading(false);
            return;
        }
        try {
            const decode = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$jwt$2d$decode$2f$build$2f$esm$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jwtDecode"])(token);
            const tokenExpiration = decode.exp;
            const now = Date.now() / 1000;
            if (tokenExpiration < now) {
                await refresh();
            } else {
                setIsAuthorized(true);
                setIsLoading(false);
            }
        } catch (error) {
            console.log("Error in Decoding", error);
            setIsAuthorized(false);
            setIsLoading(false);
        }
    };
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "ProtectedRoute.useEffect": ()=>{
            if (!isLoading && !isAuthorized) {
                router.replace("/auth/login");
            }
        }
    }["ProtectedRoute.useEffect"], [
        isLoading,
        isAuthorized,
        router
    ]);
    if (isLoading) {
        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
            className: "flex justify-center items-center min-h-screen",
            children: "Loading..."
        }, void 0, false, {
            fileName: "[project]/components/ProtectedRoute.tsx",
            lineNumber: 85,
            columnNumber: 12
        }, this);
    }
    if (!isAuthorized) {
        return null;
    }
    return children;
};
_s(ProtectedRoute, "B/mln8ED8rPPTIWPGrJw6jhD7iI=", false, function() {
    return [
        __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$navigation$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useRouter"]
    ];
});
_c = ProtectedRoute;
const __TURBOPACK__default__export__ = ProtectedRoute;
var _c;
__turbopack_refresh__.register(_c, "ProtectedRoute");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_refresh__.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
}]);

//# sourceMappingURL=_50ea1f._.js.map
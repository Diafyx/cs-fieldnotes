package org.diafyx.fieldnotes;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Color;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.view.WindowInsets;
import android.webkit.RenderProcessGoneDetail;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebBackForwardList;
import android.widget.Button;
import android.widget.FrameLayout;
import android.widget.ImageView;
import android.window.OnBackInvokedDispatcher;

import androidx.webkit.WebViewAssetLoader;
import androidx.webkit.WebViewClientCompat;

import java.io.ByteArrayInputStream;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;

public final class MainActivity extends Activity {
    private static final String HOST = "appassets.androidplatform.net";
    private static final String HOME = "https://" + HOST + "/index.html";
    private static final int LIGHT_PAPER = Color.rgb(247, 246, 242);
    private static final int DARK_PAPER = Color.rgb(16, 24, 21);
    private static final int LIGHT_SURFACE = Color.rgb(255, 254, 250);
    private static final int DARK_SURFACE = Color.rgb(23, 35, 30);
    private static final String CSP = "default-src 'self'; script-src 'self'; style-src 'self'; font-src 'self'; img-src 'self' data:; connect-src 'self'; manifest-src 'self'; worker-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'";

    private FrameLayout root;
    private FrameLayout frame;
    private View topBarBackground;
    private WebView webView;
    private ImageView backSnapshot;
    private Bitmap backBitmap;
    private final Map<String, Integer> scrollPositions = new HashMap<>();
    private String pendingBackUrl;

    @Override
    protected void onCreate(Bundle state) {
        super.onCreate(state);

        WebViewAssetLoader assets = new WebViewAssetLoader.Builder()
                .addPathHandler("/", new WebViewAssetLoader.AssetsPathHandler(this))
                .build();

        webView = new WebView(this);
        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setAllowFileAccess(false);
        settings.setAllowContentAccess(false);
        settings.setAllowFileAccessFromFileURLs(false);
        settings.setAllowUniversalAccessFromFileURLs(false);
        settings.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
        settings.setJavaScriptCanOpenWindowsAutomatically(false);
        settings.setSupportMultipleWindows(false);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            settings.setSafeBrowsingEnabled(true);
        }
        webView.setWebViewClient(new LocalOnlyClient(assets));
        root = new FrameLayout(this);
        root.setBackgroundColor(LIGHT_PAPER);
        topBarBackground = new View(this);
        topBarBackground.setBackgroundColor(LIGHT_SURFACE);
        root.addView(topBarBackground, new FrameLayout.LayoutParams(-1, 0, Gravity.TOP));
        frame = new FrameLayout(this);
        frame.setBackgroundColor(LIGHT_PAPER);
        frame.addView(webView, new FrameLayout.LayoutParams(-1, -1));
        root.addView(frame, new FrameLayout.LayoutParams(-1, -1));
        if (Build.VERSION.SDK_INT >= 35) {
            root.setOnApplyWindowInsetsListener((view, insets) -> {
                android.graphics.Insets safe = insets.getInsets(
                        WindowInsets.Type.systemBars() | WindowInsets.Type.displayCutout());
                FrameLayout.LayoutParams page = (FrameLayout.LayoutParams) frame.getLayoutParams();
                page.setMargins(safe.left, safe.top, safe.right, safe.bottom);
                frame.setLayoutParams(page);
                FrameLayout.LayoutParams top = (FrameLayout.LayoutParams) topBarBackground.getLayoutParams();
                top.height = safe.top;
                topBarBackground.setLayoutParams(top);
                return insets;
            });
        }
        setContentView(root);
        if (Build.VERSION.SDK_INT >= 33) {
            getOnBackInvokedDispatcher().registerOnBackInvokedCallback(
                    OnBackInvokedDispatcher.PRIORITY_DEFAULT, this::handleBack);
        }

        if (state == null || webView.restoreState(state) == null) {
            webView.loadUrl(HOME);
        }
    }

    @Override
    protected void onSaveInstanceState(Bundle state) {
        if (webView != null) webView.saveState(state);
        super.onSaveInstanceState(state);
    }

    @Override
    @SuppressLint("GestureBackNavigation") // Android 13 and newer use OnBackInvokedCallback above.
    @SuppressWarnings("deprecation")
    public void onBackPressed() {
        handleBack();
    }

    private void handleBack() {
        WebView current = webView;
        if (current == null) {
            finish();
            return;
        }
        if (backSnapshot != null || current.getVisibility() != View.VISIBLE) return;
        current.evaluateJavascript("Boolean(document.getElementById('search-dialog') && document.getElementById('search-dialog').open)", result -> {
            if (webView != current) return;
            if ("true".equals(result)) {
                current.evaluateJavascript("document.getElementById('search-dialog').close()", null);
            } else if (current.canGoBack()) {
                rememberScroll(current);
                WebBackForwardList history = current.copyBackForwardList();
                String target = history.getItemAtIndex(history.getCurrentIndex() - 1).getUrl();
                if (!Uri.parse(target).getPath().equals(Uri.parse(current.getUrl()).getPath())) {
                    pendingBackUrl = target;
                    showBackSnapshot(current);
                    if (backSnapshot == null) current.setVisibility(View.INVISIBLE);
                    current.postDelayed(() -> {
                        if (webView == current && (backSnapshot != null
                                || current.getVisibility() != View.VISIBLE)) {
                            pendingBackUrl = null;
                            current.setVisibility(View.VISIBLE);
                            clearBackSnapshot();
                        }
                    }, 3000);
                }
                current.goBack();
            } else {
                finish();
            }
        });
    }

    private void showBackSnapshot(WebView view) {
        if (view.getWidth() == 0 || view.getHeight() == 0) return;
        try {
            backBitmap = Bitmap.createBitmap(view.getWidth(), view.getHeight(), Bitmap.Config.RGB_565);
            view.draw(new Canvas(backBitmap));
            backSnapshot = new ImageView(this);
            backSnapshot.setImageBitmap(backBitmap);
            frame.addView(backSnapshot, new FrameLayout.LayoutParams(-1, -1));
        } catch (OutOfMemoryError error) {
            clearBackSnapshot();
        }
    }

    private void clearBackSnapshot() {
        if (backSnapshot != null) {
            frame.removeView(backSnapshot);
            backSnapshot.setImageDrawable(null);
            backSnapshot = null;
        }
        if (backBitmap != null) {
            backBitmap.recycle();
            backBitmap = null;
        }
    }

    private void rememberScroll(WebView view) {
        String url = view.getUrl();
        if (url != null) scrollPositions.put(url, view.getScrollY());
    }

    @SuppressWarnings("deprecation") // These colors still apply on Android versions before edge-to-edge.
    private void applyTheme(boolean dark) {
        int color = dark ? DARK_PAPER : LIGHT_PAPER;
        int surface = dark ? DARK_SURFACE : LIGHT_SURFACE;
        root.setBackgroundColor(color);
        frame.setBackgroundColor(color);
        topBarBackground.setBackgroundColor(surface);
        webView.setBackgroundColor(color);
        getWindow().setStatusBarColor(surface);
        getWindow().setNavigationBarColor(Build.VERSION.SDK_INT >= 27 || dark
                ? color : Color.rgb(23, 111, 91));
        View decor = getWindow().getDecorView();
        int flags = decor.getSystemUiVisibility();
        flags &= ~View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR;
        if (Build.VERSION.SDK_INT >= 26) flags &= ~View.SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR;
        if (!dark) flags |= View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR;
        if (!dark && Build.VERSION.SDK_INT >= 27) flags |= View.SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR;
        decor.setSystemUiVisibility(flags);
        if (Build.VERSION.SDK_INT >= 29) {
            getWindow().setNavigationBarContrastEnforced(false);
            getWindow().setStatusBarContrastEnforced(false);
        }
    }

    @Override
    protected void onDestroy() {
        clearBackSnapshot();
        if (webView != null) webView.destroy();
        super.onDestroy();
    }

    private boolean openExternal(Uri uri) {
        String scheme = uri.getScheme();
        if (!"https".equalsIgnoreCase(scheme) && !"http".equalsIgnoreCase(scheme)) {
            return true;
        }
        Intent intent = new Intent(Intent.ACTION_VIEW, uri);
        intent.addCategory(Intent.CATEGORY_BROWSABLE);
        try {
            startActivity(intent);
        } catch (ActivityNotFoundException ignored) {
            // The notes still work when no browser is installed.
        }
        return true;
    }

    private final class LocalOnlyClient extends WebViewClientCompat {
        private final WebViewAssetLoader assets;

        LocalOnlyClient(WebViewAssetLoader assets) {
            this.assets = assets;
        }

        @Override
        public boolean onRenderProcessGone(WebView view, RenderProcessGoneDetail detail) {
            clearBackSnapshot();
            frame.removeView(view);
            view.destroy();
            if (view == webView) webView = null;
            Button retry = new Button(MainActivity.this);
            retry.setText(R.string.reopen_app);
            retry.setOnClickListener(ignored -> recreate());
            frame.addView(retry, new FrameLayout.LayoutParams(-2, -2, Gravity.CENTER));
            return true;
        }

        @Override
        public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
            Uri uri = request.getUrl();
            if (isLocal(uri)) {
                if (request.isForMainFrame() && pendingBackUrl == null
                        && !uri.toString().equals(view.getUrl())) rememberScroll(view);
                return false;
            }
            return openExternal(uri);
        }

        @Override
        public void onPageFinished(WebView view, String url) {
            if (pendingBackUrl != null && url.equals(pendingBackUrl)) {
                pendingBackUrl = null;
                Integer saved = scrollPositions.get(url);
                view.postDelayed(() -> {
                    if (!url.equals(view.getUrl())) return;
                    if (saved != null) view.scrollTo(0, saved);
                    view.postVisualStateCallback(0, new WebView.VisualStateCallback() {
                        @Override
                        public void onComplete(long requestId) {
                            if (webView == view && url.equals(view.getUrl())) {
                                view.setVisibility(View.VISIBLE);
                                clearBackSnapshot();
                            }
                        }
                    });
                }, 120);
            }
        }

        @Override
        public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
            Uri uri = request.getUrl();
            if (!isLocal(uri)) return blocked(403, "Forbidden");
            if ("/__app_theme__/dark".equals(uri.getPath()) || "/__app_theme__/light".equals(uri.getPath())) {
                boolean dark = uri.getPath().endsWith("dark");
                runOnUiThread(() -> applyTheme(dark));
                return new WebResourceResponse("text/plain", "UTF-8", 204, "No Content",
                        new HashMap<>(), new ByteArrayInputStream(new byte[0]));
            }
            if ("/".equals(uri.getPath())) uri = uri.buildUpon().path("/index.html").build();
            WebResourceResponse response = assets.shouldInterceptRequest(uri);
            if (response == null) return blocked(404, "Not Found");
            Map<String, String> headers = new HashMap<>();
            if (response.getResponseHeaders() != null) headers.putAll(response.getResponseHeaders());
            headers.put("X-Content-Type-Options", "nosniff");
            if (uri.getPath().endsWith(".html")) {
                headers.put("Content-Security-Policy", CSP);
                headers.put("Referrer-Policy", "no-referrer");
                headers.put("X-Frame-Options", "DENY");
            }
            response.setResponseHeaders(headers);
            return response;
        }

        private boolean isLocal(Uri uri) {
            return "https".equalsIgnoreCase(uri.getScheme())
                    && HOST.equalsIgnoreCase(uri.getHost())
                    && uri.getPort() == -1
                    && uri.getUserInfo() == null;
        }

        private WebResourceResponse blocked(int code, String reason) {
            byte[] body = reason.getBytes(StandardCharsets.UTF_8);
            Map<String, String> headers = new HashMap<>();
            headers.put("X-Content-Type-Options", "nosniff");
            return new WebResourceResponse("text/plain", "UTF-8", code, reason, headers, new ByteArrayInputStream(body));
        }
    }
}

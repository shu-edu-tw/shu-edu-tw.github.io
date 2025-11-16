// Deprecated: centralized structured data injector removed.
// Per-page JSON-LD is embedded directly in each HTML file.
// This file intentionally left minimal to avoid accidental usage.

export {};

// Function to update breadcrumb schema based on current page
function updateBreadcrumbSchema(pageTitle, pageUrl) {
    const breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "首頁",
                "item": "https://shu-edu-tw.github.io/"
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": pageTitle,
                "item": pageUrl
            }
        ]
    };
    
    // Remove existing breadcrumb schema
    const existingBreadcrumb = document.getElementById('breadcrumb-schema');
    if (existingBreadcrumb) {
        existingBreadcrumb.remove();
    }
    
    // Add new breadcrumb schema
    const script = document.createElement('script');
    script.type = 'application/ld+json';
    script.textContent = JSON.stringify(breadcrumb);
    script.id = 'breadcrumb-schema';
    document.head.appendChild(script);
}

// Function to add article schema for news pages
function addArticleSchema(title, description, publishDate, imageUrl) {
    const articleSchema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description,
        "image": imageUrl,
        "datePublished": publishDate,
        "dateModified": publishDate,
        "author": {
            "@type": "Organization",
            "name": "世新大學"
        },
        "publisher": {
            "@type": "EducationalOrganization",
            "name": "世新大學",
            "logo": {
                "@type": "ImageObject",
                "url": "https://shu-edu-tw.github.io/images/shu-logo.png"
            }
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": window.location.href
        }
    };
    
    const script = document.createElement('script');
    script.type = 'application/ld+json';
    script.textContent = JSON.stringify(articleSchema);
    script.id = 'article-schema';
    document.head.appendChild(script);
}

// Initialize structured data when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    injectStructuredData();
    
    // Update page-specific schemas based on current page
    const currentPath = window.location.pathname;
    const currentUrl = window.location.href;
    
    if (currentPath.includes('about')) {
        updateBreadcrumbSchema('關於世新', currentUrl);
    } else if (currentPath.includes('colleges')) {
        updateBreadcrumbSchema('學院系所', currentUrl);
    } else if (currentPath.includes('admission')) {
        updateBreadcrumbSchema('招生資訊', currentUrl);
    } else if (currentPath.includes('campus-life')) {
        updateBreadcrumbSchema('校園生活', currentUrl);
    } else if (currentPath.includes('alumni')) {
        updateBreadcrumbSchema('傑出校友', currentUrl);
    } else if (currentPath.includes('news')) {
        updateBreadcrumbSchema('最新消息', currentUrl);
    } else if (currentPath.includes('contact')) {
        updateBreadcrumbSchema('聯絡我們', currentUrl);
    }
});

// Export functions for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        injectStructuredData,
        updateBreadcrumbSchema,
        addArticleSchema,
        organizationSchema,
        websiteSchema,
        faqSchema
    };
}


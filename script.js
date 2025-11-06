// 移动端菜单切换
const menuToggle = document.querySelector('.menu-toggle');
const navMenu = document.querySelector('.nav-menu');

menuToggle.addEventListener('click', () => {
    navMenu.classList.toggle('active');
});

// 点击菜单项后关闭移动端菜单
const navLinks = document.querySelectorAll('.nav-menu a');
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        navMenu.classList.remove('active');
    });
});

// 平滑滚动到锚点
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const offsetTop = target.offsetTop - 70; // 减去导航栏高度
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    });
});

// 滚动时添加导航栏阴影效果
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)';
    } else {
        navbar.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
    }
});

// 加载资源数据
async function loadResources() {
    try {
        console.log('开始加载资源...');
        const response = await fetch('resources.json');
        console.log('Response status:', response.status);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('资源数据加载成功:', data);
        renderResources(data);
    } catch (error) {
        console.error('加载资源失败:', error);
        // 显示错误提示
        document.querySelectorAll('.resource-grid').forEach(grid => {
            grid.innerHTML = '<div class="resource-card"><h3>⚠️ 资源加载失败</h3><p>请稍后刷新页面重试</p></div>';
        });
    }
}

// 渲染资源到页面
function renderResources(data) {
    data.categories.forEach(category => {
        const section = document.getElementById(category.id);
        if (!section) return;

        const container = section.querySelector('.resource-grid');
        container.innerHTML = ''; // 清空现有内容

        if (category.hasSubcategories) {
            // 有二级分类的情况
            category.subcategories.forEach(subcategory => {
                if (subcategory.resources && subcategory.resources.length > 0) {
                    // 创建子分类标题
                    const subcatTitle = document.createElement('h3');
                    subcatTitle.className = 'col-span-full text-xl font-semibold text-gray-700 mt-4 mb-2';
                    subcatTitle.textContent = subcategory.name;
                    container.appendChild(subcatTitle);

                    // 渲染该子分类下的资源
                    subcategory.resources.forEach(resource => {
                        const card = createResourceCard(resource);
                        container.appendChild(card);
                    });
                }
            });
        } else {
            // 没有二级分类，直接渲染资源
            if (category.resources && category.resources.length > 0) {
                category.resources.forEach(resource => {
                    const card = createResourceCard(resource);
                    container.appendChild(card);
                });
            }
        }
    });

    // 重新初始化动画观察器
    initCardAnimations();
}

// 创建资源卡片
function createResourceCard(resource) {
    const card = document.createElement('div');
    card.className = 'resource-card';
    
    card.innerHTML = `
        <h3>${resource.title}</h3>
        <p>${resource.description}</p>
        ${resource.subscribers ? `<p class="text-sm text-gray-500">👥 ${resource.subscribers}</p>` : ''}
        ${resource.members ? `<p class="text-sm text-gray-500">👥 ${resource.members}</p>` : ''}
        ${resource.username ? `<p class="text-sm text-gray-500">用户名: ${resource.username}</p>` : ''}
        ${resource.contact ? `<p class="text-sm text-gray-500">联系: ${resource.contact}</p>` : ''}
        <a href="${resource.link}" class="btn" target="_blank" rel="noopener">访问</a>
    `;
    
    return card;
}

// 初始化卡片动画
function initCardAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '0';
                entry.target.style.transform = 'translateY(20px)';
                
                setTimeout(() => {
                    entry.target.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, 100);
                
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.resource-card').forEach(card => {
        observer.observe(card);
    });
}

// 页面加载时加载资源
document.addEventListener('DOMContentLoaded', loadResources);

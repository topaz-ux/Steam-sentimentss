"""
Steam 리뷰 감정 분석 시각화 스크립트
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from collections import Counter

# wordcloud는 선택적 (컴파일러가 필요한 경우 설치 실패할 수 있음)
try:
    from wordcloud import WordCloud
    WORDCLOUD_AVAILABLE = True
except ImportError:
    WORDCLOUD_AVAILABLE = False
    # 경고 메시지는 조용히 처리 (필요시 주석 해제)
    # print("경고: wordcloud가 설치되지 않았습니다. 워드 클라우드 기능을 건너뜁니다.")

# 한글 폰트 설정 (Windows)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

def load_data(csv_file='game_reviews.csv'):
    """CSV 파일에서 데이터 로드"""
    try:
        df = pd.read_csv(csv_file, encoding='utf-8-sig')
        return df
    except FileNotFoundError:
        print(f"파일 '{csv_file}'을 찾을 수 없습니다.")
        return None

def plot_recommendation_distribution(df):
    """추천 분포 막대 그래프"""
    plt.figure(figsize=(10, 6))
    recommendation_counts = df['recommended'].value_counts()
    labels = ['추천', '비추천']
    colors = ['#2ecc71', '#e74c3c']
    
    plt.bar(labels, [recommendation_counts.get(True, 0), recommendation_counts.get(False, 0)], 
            color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
    plt.title('Steam 리뷰 추천 분포', fontsize=16, fontweight='bold', pad=20)
    plt.ylabel('리뷰 수', fontsize=12)
    plt.xlabel('추천 여부', fontsize=12)
    
    # 값 표시
    for i, (label, count) in enumerate(zip(labels, [recommendation_counts.get(True, 0), recommendation_counts.get(False, 0)])):
        plt.text(i, count + max(recommendation_counts) * 0.01, str(count), 
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('recommendation_distribution.png', dpi=300, bbox_inches='tight')
    print("추천 분포 그래프가 'recommendation_distribution.png'에 저장되었습니다.")
    plt.close()

def plot_sentiment_boxplot(df):
    """감정 점수 박스 플롯"""
    plt.figure(figsize=(12, 7))
    
    # 추천/비추천별로 데이터 분리
    recommended_scores = df[df['recommended']]['compound_score'].values
    not_recommended_scores = df[~df['recommended']]['compound_score'].values
    
    data_to_plot = [recommended_scores, not_recommended_scores]
    labels = ['추천', '비추천']
    
    bp = plt.boxplot(data_to_plot, labels=labels, patch_artist=True, 
                     widths=0.6, showmeans=True, meanline=True)
    
    # 박스 색상 설정
    colors = ['#2ecc71', '#e74c3c']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    # 중앙선 스타일 설정
    for median in bp['medians']:
        median.set(color='black', linewidth=2)
    
    plt.title('추천 여부별 감정 점수 분포 (Compound Score)', fontsize=16, fontweight='bold', pad=20)
    plt.ylabel('Compound Score', fontsize=12)
    plt.xlabel('추천 여부', fontsize=12)
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    
    plt.tight_layout()
    plt.savefig('sentiment_boxplot.png', dpi=300, bbox_inches='tight')
    print("감정 점수 박스 플롯이 'sentiment_boxplot.png'에 저장되었습니다.")
    plt.close()

def plot_sentiment_distribution(df):
    """감정 레이블 분포"""
    plt.figure(figsize=(10, 6))
    sentiment_counts = df['sentiment_label'].value_counts()
    colors_map = {'positive': '#2ecc71', 'negative': '#e74c3c', 'neutral': '#f39c12'}
    colors = [colors_map.get(label, '#95a5a6') for label in sentiment_counts.index]
    
    bars = plt.bar(sentiment_counts.index, sentiment_counts.values, 
                   color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
    
    plt.title('감정 레이블 분포', fontsize=16, fontweight='bold', pad=20)
    plt.ylabel('리뷰 수', fontsize=12)
    plt.xlabel('감정 레이블', fontsize=12)
    
    # 값 표시
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + max(sentiment_counts) * 0.01,
                f'{int(height)}', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('sentiment_distribution.png', dpi=300, bbox_inches='tight')
    print("감정 분포 그래프가 'sentiment_distribution.png'에 저장되었습니다.")
    plt.close()

def create_wordcloud(df, background_color='white', max_words=100):
    """워드 클라우드 생성"""
    if not WORDCLOUD_AVAILABLE:
        print("워드 클라우드를 생성할 수 없습니다. wordcloud 패키지가 설치되지 않았습니다.")
        print("설치하려면: pip install wordcloud (컴파일러 필요)")
        return
    
    # 모든 리뷰 텍스트 결합
    if 'cleaned_text' in df.columns:
        text = ' '.join(df['cleaned_text'].dropna().astype(str))
    else:
        text = ' '.join(df['review_text'].dropna().astype(str))
    
    if not text.strip():
        print("워드 클라우드를 생성할 텍스트가 없습니다.")
        return
    
    # 워드 클라우드 생성
    wordcloud = WordCloud(width=1200, height=600, 
                         background_color=background_color,
                         max_words=max_words,
                         colormap='viridis',
                         relative_scaling=0.5,
                         random_state=42).generate(text)
    
    plt.figure(figsize=(15, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Steam 리뷰 워드 클라우드', fontsize=20, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('wordcloud.png', dpi=300, bbox_inches='tight')
    print("워드 클라우드가 'wordcloud.png'에 저장되었습니다.")
    plt.close()

def plot_playtime_vs_sentiment(df):
    """플레이 시간과 감정 점수의 관계"""
    plt.figure(figsize=(12, 7))
    
    plt.scatter(df['playtime_at_review'], df['compound_score'], 
               alpha=0.6, s=50, c=df['recommended'].map({True: '#2ecc71', False: '#e74c3c'}))
    
    plt.title('플레이 시간 vs 감정 점수', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('플레이 시간 (시간)', fontsize=12)
    plt.ylabel('Compound Score', fontsize=12)
    plt.grid(alpha=0.3, linestyle='--')
    plt.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    
    # 범례
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='#2ecc71', label='추천'),
                      Patch(facecolor='#e74c3c', label='비추천')]
    plt.legend(handles=legend_elements, loc='best')
    
    plt.tight_layout()
    plt.savefig('playtime_vs_sentiment.png', dpi=300, bbox_inches='tight')
    print("플레이 시간 vs 감정 점수 그래프가 'playtime_vs_sentiment.png'에 저장되었습니다.")
    plt.close()

def plot_sentiment_pie_chart(df):
    """감정 분포 파이 차트"""
    plt.figure(figsize=(10, 8))
    
    sentiment_counts = df['sentiment_label'].value_counts()
    colors_map = {'positive': '#2ecc71', 'negative': '#e74c3c', 'neutral': '#f39c12'}
    colors = [colors_map.get(label, '#95a5a6') for label in sentiment_counts.index]
    
    # 한글 레이블
    labels_map = {'positive': '긍정', 'negative': '부정', 'neutral': '중립'}
    labels = [labels_map.get(label, label) for label in sentiment_counts.index]
    
    # 파이 차트 생성
    wedges, texts, autotexts = plt.pie(sentiment_counts.values, 
                                        labels=labels,
                                        colors=colors,
                                        autopct='%1.1f%%',
                                        startangle=90,
                                        textprops={'fontsize': 12, 'fontweight': 'bold'})
    
    plt.title('감정 분포 (파이 차트)', fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('sentiment_pie_chart.png', dpi=300, bbox_inches='tight')
    print("감정 분포 파이 차트가 'sentiment_pie_chart.png'에 저장되었습니다.")
    plt.close()

def plot_review_length_distribution(df):
    """리뷰 길이 분포 히스토그램"""
    plt.figure(figsize=(12, 7))
    
    # 리뷰 길이 데이터
    review_lengths = df['review_length'].values
    
    plt.hist(review_lengths, bins=30, color='#3498db', alpha=0.7, edgecolor='black')
    plt.title('리뷰 길이 분포', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('리뷰 길이 (문자 수)', fontsize=12)
    plt.ylabel('리뷰 수', fontsize=12)
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    
    # 통계 정보 표시
    mean_length = review_lengths.mean()
    median_length = np.median(review_lengths)
    plt.axvline(mean_length, color='red', linestyle='--', linewidth=2, label=f'평균: {mean_length:.1f}')
    plt.axvline(median_length, color='green', linestyle='--', linewidth=2, label=f'중앙값: {median_length:.1f}')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('review_length_distribution.png', dpi=300, bbox_inches='tight')
    print("리뷰 길이 분포 히스토그램이 'review_length_distribution.png'에 저장되었습니다.")
    plt.close()

def plot_sentiment_score_histogram(df):
    """감정 점수 히스토그램"""
    plt.figure(figsize=(12, 7))
    
    # 추천/비추천별로 히스토그램
    recommended_scores = df[df['recommended']]['compound_score'].values
    not_recommended_scores = df[~df['recommended']]['compound_score'].values
    
    plt.hist(recommended_scores, bins=30, alpha=0.6, label='추천', color='#2ecc71', edgecolor='black')
    plt.hist(not_recommended_scores, bins=30, alpha=0.6, label='비추천', color='#e74c3c', edgecolor='black')
    
    plt.title('감정 점수 분포 (히스토그램)', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Compound Score', fontsize=12)
    plt.ylabel('리뷰 수', fontsize=12)
    plt.legend()
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.axvline(x=0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
    
    plt.tight_layout()
    plt.savefig('sentiment_score_histogram.png', dpi=300, bbox_inches='tight')
    print("감정 점수 히스토그램이 'sentiment_score_histogram.png'에 저장되었습니다.")
    plt.close()

def plot_playtime_distribution(df):
    """플레이 시간 분포 (추천/비추천별)"""
    if 'playtime_at_review' not in df.columns:
        return
    
    plt.figure(figsize=(12, 7))
    
    recommended_playtime = df[df['recommended']]['playtime_at_review'].values
    not_recommended_playtime = df[~df['recommended']]['playtime_at_review'].values
    
    plt.hist(recommended_playtime, bins=30, alpha=0.6, label='추천', color='#2ecc71', edgecolor='black')
    plt.hist(not_recommended_playtime, bins=30, alpha=0.6, label='비추천', color='#e74c3c', edgecolor='black')
    
    plt.title('플레이 시간 분포 (추천/비추천별)', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('플레이 시간 (시간)', fontsize=12)
    plt.ylabel('리뷰 수', fontsize=12)
    plt.legend()
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig('playtime_distribution.png', dpi=300, bbox_inches='tight')
    print("플레이 시간 분포 그래프가 'playtime_distribution.png'에 저장되었습니다.")
    plt.close()

def plot_date_sentiment_trend(df):
    """날짜별 감정 점수 추이"""
    if 'date_posted' not in df.columns:
        return
    
    try:
        # 날짜 변환
        df['date'] = pd.to_datetime(df['date_posted'], errors='coerce')
        df_with_date = df.dropna(subset=['date'])
        
        if df_with_date.empty:
            return
        
        # 날짜별 평균 감정 점수
        daily_sentiment = df_with_date.groupby(df_with_date['date'].dt.date)['compound_score'].mean().sort_index()
        
        plt.figure(figsize=(14, 7))
        plt.plot(daily_sentiment.index, daily_sentiment.values, marker='o', linewidth=2, markersize=6, color='#3498db')
        plt.fill_between(daily_sentiment.index, daily_sentiment.values, alpha=0.3, color='#3498db')
        
        plt.title('날짜별 평균 감정 점수 추이', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('날짜', fontsize=12)
        plt.ylabel('평균 Compound Score', fontsize=12)
        plt.grid(alpha=0.3, linestyle='--')
        plt.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig('date_sentiment_trend.png', dpi=300, bbox_inches='tight')
        print("날짜별 감정 점수 추이가 'date_sentiment_trend.png'에 저장되었습니다.")
        plt.close()
    except Exception as e:
        print(f"날짜별 추이 그래프 생성 오류: {e}")

def create_simple_wordcloud(df):
    """간단한 워드 클라우드 (wordcloud 없이 matplotlib만 사용)"""
    if 'cleaned_text' in df.columns:
        text = ' '.join(df['cleaned_text'].dropna().astype(str))
    else:
        text = ' '.join(df['review_text'].dropna().astype(str))
    
    if not text.strip():
        print("워드 클라우드를 생성할 텍스트가 없습니다.")
        return
    
    # 단어 빈도 계산
    words = text.lower().split()
    # 짧은 단어 제거
    words = [w for w in words if len(w) > 3]
    
    from collections import Counter
    word_freq = Counter(words)
    top_words = word_freq.most_common(50)
    
    # 간단한 텍스트 기반 시각화
    plt.figure(figsize=(15, 8))
    
    # 상위 단어들을 크기별로 표시
    y_pos = np.arange(len(top_words[:30]))
    word_counts = [count for word, count in top_words[:30]]
    words_list = [word for word, count in top_words[:30]]
    
    plt.barh(y_pos, word_counts, color='#3498db', alpha=0.7)
    plt.yticks(y_pos, words_list)
    plt.xlabel('빈도', fontsize=12)
    plt.title('상위 단어 빈도 (워드 클라우드 대체)', fontsize=16, fontweight='bold', pad=20)
    plt.gca().invert_yaxis()
    
    plt.tight_layout()
    plt.savefig('wordcloud_simple.png', dpi=300, bbox_inches='tight')
    print("간단한 단어 빈도 그래프가 'wordcloud_simple.png'에 저장되었습니다.")
    plt.close()

def generate_all_visualizations(csv_file='game_reviews.csv'):
    """모든 시각화 생성"""
    df = load_data(csv_file)
    
    if df is None:
        return
    
    print("\n=== 시각화 생성 시작 ===\n")
    
    # 1. 추천 분포
    try:
        plot_recommendation_distribution(df)
    except Exception as e:
        print(f"추천 분포 그래프 생성 오류: {e}")
    
    # 2. 감정 점수 박스 플롯
    try:
        plot_sentiment_boxplot(df)
    except Exception as e:
        print(f"감정 점수 박스 플롯 생성 오류: {e}")
    
    # 3. 감정 레이블 분포
    try:
        plot_sentiment_distribution(df)
    except Exception as e:
        print(f"감정 레이블 분포 그래프 생성 오류: {e}")
    
    # 4. 워드 클라우드 (선택적, 실패해도 계속 진행)
    if WORDCLOUD_AVAILABLE:
        try:
            create_wordcloud(df)
        except Exception as e:
            print(f"워드 클라우드 생성 오류 (건너뜀): {e}")
            # 대체 방법 사용
            try:
                create_simple_wordcloud(df)
            except Exception as e2:
                print(f"간단한 워드 클라우드 생성 오류: {e2}")
    else:
        # wordcloud가 없으면 간단한 버전 사용
        try:
            create_simple_wordcloud(df)
        except Exception as e:
            print(f"간단한 워드 클라우드 생성 오류: {e}")
    
    # 5. 플레이 시간 vs 감정 점수
    if 'playtime_at_review' in df.columns:
        try:
            plot_playtime_vs_sentiment(df)
        except Exception as e:
            print(f"플레이 시간 vs 감정 점수 그래프 생성 오류: {e}")
    
    # 6. 감정 분포 파이 차트
    try:
        plot_sentiment_pie_chart(df)
    except Exception as e:
        print(f"감정 분포 파이 차트 생성 오류: {e}")
    
    # 7. 리뷰 길이 분포
    try:
        plot_review_length_distribution(df)
    except Exception as e:
        print(f"리뷰 길이 분포 그래프 생성 오류: {e}")
    
    # 8. 감정 점수 히스토그램
    try:
        plot_sentiment_score_histogram(df)
    except Exception as e:
        print(f"감정 점수 히스토그램 생성 오류: {e}")
    
    # 9. 플레이 시간 분포
    if 'playtime_at_review' in df.columns:
        try:
            plot_playtime_distribution(df)
        except Exception as e:
            print(f"플레이 시간 분포 그래프 생성 오류: {e}")
    
    # 10. 날짜별 감정 추이
    try:
        plot_date_sentiment_trend(df)
    except Exception as e:
        print(f"날짜별 감정 추이 그래프 생성 오류: {e}")
    
    print("\n=== 시각화 생성이 완료되었습니다! ===\n")

if __name__ == "__main__":
    generate_all_visualizations()


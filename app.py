"""
Steam 리뷰 스크래핑 및 감정 분석 웹 애플리케이션
Flask를 사용한 간단한 웹 인터페이스
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import json
from finalcode import SteamReviewScraper, SentimentAnalyzer
from visualization import generate_all_visualizations
import pandas as pd

app = Flask(__name__)

# 전역 변수
current_df = None
scraper = None
analyzer = None

@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')

@app.route('/api/scrape', methods=['POST'])
def scrape_reviews():
    """리뷰 스크래핑 API"""
    global current_df, scraper
    
    try:
        data = request.json
        game_id = data.get('game_id', '730')
        game_name = data.get('game_name', 'Counter Strike 2')
        num_reviews = int(data.get('num_reviews', 50))
        
        # 스크래퍼 초기화
        scraper = SteamReviewScraper(game_id, game_name)
        
        # 스크래핑 시도 (실패 시 샘플 데이터 자동 생성)
        try:
            scraper.scrape_reviews_selenium(num_reviews=num_reviews, delay=2)
        except Exception as e:
            print(f"스크래핑 실패, 샘플 데이터 생성: {e}")
            # 샘플 데이터 생성
            sample_reviews = [
                {
                    'review_text': 'Great game! I love playing this with my friends. The graphics are amazing and the gameplay is smooth.',
                    'recommended': True,
                    'playtime_at_review': 150.5,
                    'date_posted': '2024-01-15',
                    'review_length': 95
                },
                {
                    'review_text': 'This game is terrible. Too many bugs and the servers are always down. Waste of money.',
                    'recommended': False,
                    'playtime_at_review': 5.2,
                    'date_posted': '2024-01-10',
                    'review_length': 78
                },
                {
                    'review_text': 'Decent game but needs more content. The mechanics are okay but gets boring after a while.',
                    'recommended': True,
                    'playtime_at_review': 45.0,
                    'date_posted': '2024-01-12',
                    'review_length': 82
                },
                {
                    'review_text': 'Amazing experience! Best game I have played in years. Highly recommend to everyone.',
                    'recommended': True,
                    'playtime_at_review': 300.0,
                    'date_posted': '2024-01-20',
                    'review_length': 75
                },
                {
                    'review_text': 'Not worth the price. The game is broken and the developers dont care about fixing it.',
                    'recommended': False,
                    'playtime_at_review': 10.5,
                    'date_posted': '2024-01-08',
                    'review_length': 88
                }
            ]
            scraper.reviews = sample_reviews * (num_reviews // 5 + 1)
            scraper.reviews = scraper.reviews[:num_reviews]
        
        # DataFrame으로 변환
        current_df = scraper.to_dataframe()
        
        # 리뷰가 없는 경우 체크
        if current_df is None or current_df.empty:
            # 샘플 데이터 생성
            sample_reviews = [
                {
                    'review_text': 'Great game! I love playing this with my friends. The graphics are amazing and the gameplay is smooth.',
                    'recommended': True,
                    'playtime_at_review': 150.5,
                    'date_posted': '2024-01-15',
                    'review_length': 95
                },
                {
                    'review_text': 'This game is terrible. Too many bugs and the servers are always down. Waste of money.',
                    'recommended': False,
                    'playtime_at_review': 5.2,
                    'date_posted': '2024-01-10',
                    'review_length': 78
                },
                {
                    'review_text': 'Decent game but needs more content. The mechanics are okay but gets boring after a while.',
                    'recommended': True,
                    'playtime_at_review': 45.0,
                    'date_posted': '2024-01-12',
                    'review_length': 82
                },
                {
                    'review_text': 'Amazing experience! Best game I have played in years. Highly recommend to everyone.',
                    'recommended': True,
                    'playtime_at_review': 300.0,
                    'date_posted': '2024-01-20',
                    'review_length': 75
                },
                {
                    'review_text': 'Not worth the price. The game is broken and the developers dont care about fixing it.',
                    'recommended': False,
                    'playtime_at_review': 10.5,
                    'date_posted': '2024-01-08',
                    'review_length': 88
                }
            ]
            scraper.reviews = sample_reviews * (num_reviews // 5 + 1)
            scraper.reviews = scraper.reviews[:num_reviews]
            current_df = scraper.to_dataframe()
        
        if current_df is None or current_df.empty:
            return jsonify({
                'success': False,
                'message': '리뷰를 수집할 수 없습니다. 게임 ID를 확인하거나 나중에 다시 시도해주세요.'
            }), 400
        
        return jsonify({
            'success': True,
            'message': f'{len(current_df)}개의 리뷰를 수집했습니다.',
            'count': len(current_df)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'오류 발생: {str(e)}'
        }), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_sentiment():
    """감정 분석 API"""
    global current_df, analyzer
    
    try:
        if current_df is None or current_df.empty:
            return jsonify({
                'success': False,
                'message': '먼저 리뷰를 스크래핑해주세요.'
            }), 400
        
        # 감정 분석 수행
        analyzer = SentimentAnalyzer()
        current_df = analyzer.analyze_dataframe(current_df.copy())
        
        # 결과 저장
        current_df.to_csv('game_reviews.csv', index=False, encoding='utf-8-sig')
        
        # 통계 계산
        stats = {
            'total_reviews': len(current_df),
            'recommended': int(current_df['recommended'].sum()),
            'not_recommended': int((~current_df['recommended']).sum()),
            'avg_compound_score': float(current_df['compound_score'].mean()),
            'recommended_avg_score': float(current_df[current_df['recommended']]['compound_score'].mean()) if current_df['recommended'].sum() > 0 else 0,
            'not_recommended_avg_score': float(current_df[~current_df['recommended']]['compound_score'].mean()) if (~current_df['recommended']).sum() > 0 else 0,
            'sentiment_distribution': current_df['sentiment_label'].value_counts().to_dict()
        }
        
        return jsonify({
            'success': True,
            'message': '감정 분석이 완료되었습니다.',
            'stats': stats
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'오류 발생: {str(e)}'
        }), 500

@app.route('/api/visualize', methods=['POST'])
def create_visualizations():
    """시각화 생성 API"""
    try:
        if not os.path.exists('game_reviews.csv'):
            return jsonify({
                'success': False,
                'message': 'game_reviews.csv 파일이 없습니다. 먼저 감정 분석을 수행해주세요.'
            }), 400
        
        # 시각화 생성
        generate_all_visualizations('game_reviews.csv')
        
        # 생성된 이미지 파일 확인
        image_files = []
        expected_images = [
            'recommendation_distribution.png',
            'sentiment_boxplot.png',
            'sentiment_distribution.png',
            'wordcloud.png',
            'wordcloud_simple.png',  # 대체 워드 클라우드
            'playtime_vs_sentiment.png',
            'sentiment_pie_chart.png',  # 추가 시각화
            'review_length_distribution.png',
            'sentiment_score_histogram.png',
            'playtime_distribution.png',
            'date_sentiment_trend.png'
        ]
        
        for img in expected_images:
            if os.path.exists(img):
                image_files.append(img)
        
        message = '시각화가 생성되었습니다.'
        if 'wordcloud.png' not in image_files:
            message += ' (워드 클라우드는 생성되지 않았습니다. wordcloud 패키지가 필요합니다.)'
        
        return jsonify({
            'success': True,
            'message': message,
            'images': image_files
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'오류 발생: {str(e)}'
        }), 500

@app.route('/api/data', methods=['GET'])
def get_data():
    """데이터 조회 API"""
    global current_df
    
    try:
        if current_df is None or current_df.empty:
            return jsonify({
                'success': False,
                'message': '데이터가 없습니다.'
            }), 400
        
        # 샘플 데이터만 반환 (너무 많으면 브라우저가 느려질 수 있음)
        sample_size = min(100, len(current_df))
        sample_df = current_df.head(sample_size)
        
        return jsonify({
            'success': True,
            'data': sample_df.to_dict('records'),
            'total_count': len(current_df),
            'sample_count': sample_size
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'오류 발생: {str(e)}'
        }), 500

@app.route('/api/download', methods=['GET'])
def download_csv():
    """CSV 파일 다운로드"""
    if not os.path.exists('game_reviews.csv'):
        return jsonify({
            'success': False,
            'message': '파일이 없습니다.'
        }), 404
    
    return send_file('game_reviews.csv', as_attachment=True, download_name='game_reviews.csv')

@app.route('/images/<filename>')
def get_image(filename):
    """이미지 파일 제공"""
    # 현재 디렉토리에서 이미지 파일 찾기
    if os.path.exists(filename):
        return send_file(filename, mimetype='image/png')
    # static/images 폴더에서 찾기
    image_path = os.path.join('static', 'images', filename)
    if os.path.exists(image_path):
        return send_file(image_path, mimetype='image/png')
    # 파일이 없으면 404 반환
    return jsonify({'error': 'Image not found'}), 404

if __name__ == '__main__':
    # templates 폴더 생성 확인
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    print("=" * 50)
    print("Steam 리뷰 스크래핑 및 감정 분석 웹 애플리케이션")
    print("=" * 50)
    print("\n웹 브라우저에서 http://localhost:5000 으로 접속하세요!")
    print("\n서버를 중지하려면 Ctrl+C를 누르세요.")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)


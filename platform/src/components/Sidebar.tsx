import React, { useState, useEffect, useRef } from 'react';
import { Course } from '../types';
import { MathText } from './MathText';

interface SidebarProps {
  course: Course;
  selectedUnitIndex: number | null;
  isCourseChallengeActive: boolean;
  onSelectUnit: (index: number) => void;
  onSelectCourseChallenge: () => void;
  onBackToLibrary: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  course,
  selectedUnitIndex,
  isCourseChallengeActive,
  onSelectUnit,
  onSelectCourseChallenge,
  onBackToLibrary,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [isDesktop, setIsDesktop] = useState(() =>
    typeof window !== 'undefined' ? window.innerWidth >= 1024 : false
  );

  const asideRef = useRef<HTMLElement>(null);
  const toggleButtonRef = useRef<HTMLButtonElement>(null);
  const closeButtonRef = useRef<HTMLButtonElement>(null);
  const prevOpenRef = useRef(isOpen);

  const units = course.competencies;

  // Track desktop breakpoint (>= 1024px) and auto-close drawer on resize
  useEffect(() => {
    const handleResize = () => {
      const desktop = window.innerWidth >= 1024;
      setIsDesktop(desktop);
      if (desktop && isOpen) {
        setIsOpen(false);
      }
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [isOpen]);

  // Body scroll lock with scrollbar compensation when drawer is open
  useEffect(() => {
    if (!isOpen) return;

    const originalOverflow = document.body.style.overflow;
    const originalPaddingRight = document.body.style.paddingRight;
    const scrollbarWidth = window.innerWidth - document.documentElement.clientWidth;

    if (scrollbarWidth > 0) {
      document.body.style.paddingRight = `${scrollbarWidth}px`;
    }
    document.body.style.overflow = 'hidden';

    return () => {
      document.body.style.overflow = originalOverflow;
      document.body.style.paddingRight = originalPaddingRight;
    };
  }, [isOpen]);

  // Focus trap & keyboard navigation (Escape + Tab cycling)
  useEffect(() => {
    if (!isOpen) return;

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        e.preventDefault();
        setIsOpen(false);
        toggleButtonRef.current?.focus();
        return;
      }

      if (e.key === 'Tab') {
        const aside = asideRef.current;
        if (!aside) return;

        const focusableElements = aside.querySelectorAll<HTMLElement>(
          'button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
        );

        if (focusableElements.length === 0) {
          e.preventDefault();
          return;
        }

        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];

        if (e.shiftKey) {
          if (document.activeElement === firstElement || !aside.contains(document.activeElement)) {
            e.preventDefault();
            lastElement.focus();
          }
        } else {
          if (document.activeElement === lastElement || !aside.contains(document.activeElement)) {
            e.preventDefault();
            firstElement.focus();
          }
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen]);

  // Manage focus transitions between toggle button and drawer
  useEffect(() => {
    if (isOpen && !prevOpenRef.current) {
      const timer = setTimeout(() => {
        if (closeButtonRef.current) {
          closeButtonRef.current.focus();
        } else {
          const first = asideRef.current?.querySelector<HTMLElement>(
            'button:not([disabled]), [href], [tabindex]:not([tabindex="-1"])'
          );
          first?.focus();
        }
      }, 30);
      return () => clearTimeout(timer);
    } else if (!isOpen && prevOpenRef.current) {
      toggleButtonRef.current?.focus();
    }
    prevOpenRef.current = isOpen;
  }, [isOpen]);

  const handleSelectUnit = (idx: number) => {
    setIsOpen(false);
    onSelectUnit(idx);
  };

  const handleSelectCourseChallenge = () => {
    setIsOpen(false);
    onSelectCourseChallenge();
  };

  const handleBackToLibrary = () => {
    setIsOpen(false);
    onBackToLibrary();
  };

  // When drawer is closed on mobile (< 1024px), make inner items unfocusable
  const itemTabIndex = !isDesktop && !isOpen ? -1 : undefined;

  return (
    <>
      {/* Mobile hamburger toggle button */}
      <button
        ref={toggleButtonRef}
        type="button"
        data-testid="sidebar-toggle"
        aria-label={isOpen ? 'Close sidebar' : 'Open sidebar'}
        aria-expanded={isOpen}
        aria-controls="sidebar"
        onClick={() => setIsOpen((prev) => !prev)}
        className="lg:hidden fixed top-3 left-4 z-40 p-2.5 rounded-lg bg-white border border-ka-border-subtle shadow-sm hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-ka-blue text-ka-text-primary flex items-center justify-center transition-colors"
      >
        <svg
          className="w-5 h-5 text-ka-text-primary"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          strokeWidth={2}
          aria-hidden="true"
        >
          {isOpen ? (
            <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
          ) : (
            <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" />
          )}
        </svg>
      </button>

      {/* Backdrop overlay for mobile drawer */}
      {isOpen && (
        <div
          className="lg:hidden fixed inset-0 bg-black/40 z-40 cursor-pointer transition-opacity backdrop-blur-[1px]"
          onClick={() => setIsOpen(false)}
          aria-hidden="true"
        />
      )}

      {/* Sidebar navigation drawer / desktop sidebar */}
      <aside
        ref={asideRef}
        id="sidebar"
        data-testid="sidebar"
        aria-label="Course navigation"
        role={!isDesktop && isOpen ? 'dialog' : undefined}
        aria-modal={!isDesktop && isOpen ? 'true' : undefined}
        aria-hidden={!isDesktop && !isOpen ? 'true' : undefined}
        className={`fixed lg:static inset-y-0 left-0 z-50 w-64 max-w-[85vw] lg:w-56 xl:w-64 flex-shrink-0 bg-white border-r border-ka-border-subtle min-h-screen py-6 flex flex-col transition-transform duration-200 ease-in-out shadow-xl lg:shadow-none ${
          isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        }`}
      >
        {/* Back to courses */}
        <div className="flex items-center justify-between px-6 mb-4">
          <button
            onClick={handleBackToLibrary}
            tabIndex={itemTabIndex}
            className="text-xs font-semibold text-ka-blue hover:text-ka-blue-hover flex items-center gap-1.5 transition-colors focus:outline-none focus:underline"
          >
            <span>←</span>
            <span>Course Library</span>
          </button>
          <button
            ref={closeButtonRef}
            type="button"
            aria-label="Close sidebar"
            onClick={() => setIsOpen(false)}
            tabIndex={itemTabIndex}
            className="lg:hidden p-1 -mr-2 text-ka-text-secondary hover:text-ka-text-primary rounded-md hover:bg-slate-100 focus:outline-none focus:ring-2 focus:ring-ka-blue"
          >
            <svg
              className="w-5 h-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2}
              aria-hidden="true"
            >
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Course Header */}
        <div className="px-6 pb-5 border-b border-ka-border-subtle">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-cyan-500 text-white flex items-center justify-center font-bold text-lg shadow-sm shrink-0">
              {course.title.charAt(0)}
            </div>
            <div className="flex-1 min-w-0">
              <h2 className="text-sm font-bold text-ka-text-primary leading-tight truncate block max-w-full">
                <MathText text={course.title} inline />
              </h2>
              <div className="mt-1">
                <span className="inline-block px-2 py-0.5 bg-slate-100 text-slate-700 text-[11px] font-bold rounded">
                  {units.length} UNITS
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Units List */}
        <nav className="flex-1 overflow-y-auto py-2 overscroll-contain">
          {units.map((unit, idx) => {
            const isActive = selectedUnitIndex === idx && !isCourseChallengeActive;
            return (
              <button
                key={unit.id}
                onClick={() => handleSelectUnit(idx)}
                tabIndex={itemTabIndex}
                className={`w-full text-left px-6 py-3 border-b border-ka-border-subtle transition-colors flex flex-col justify-center focus:outline-none focus:bg-slate-100 ${
                  isActive
                    ? 'bg-ka-blue-light border-l-4 border-l-ka-blue text-ka-blue'
                    : 'hover:bg-slate-50 text-ka-text-primary'
                }`}
              >
                <span className="text-[11px] font-bold tracking-wider text-slate-500 uppercase">
                  UNIT {idx + 1}
                </span>
                <span
                  className={`text-sm font-medium mt-0.5 block max-w-full truncate ${
                    isActive ? 'text-ka-blue font-semibold' : 'text-ka-text-primary'
                  }`}
                >
                  <MathText text={unit.name} inline />
                </span>
              </button>
            );
          })}

          {/* Course Challenge Item */}
          <button
            onClick={handleSelectCourseChallenge}
            tabIndex={itemTabIndex}
            className={`w-full text-left px-6 py-3 mt-2 border-t border-b border-ka-border-subtle transition-colors flex items-start gap-3 focus:outline-none focus:bg-slate-100 ${
              isCourseChallengeActive
                ? 'bg-ka-blue-light border-l-4 border-l-ka-blue text-ka-blue'
                : 'hover:bg-slate-50 text-ka-text-primary'
            }`}
          >
            <span className="text-xl leading-none shrink-0">📖</span>
            <div className="flex-1 min-w-0">
              <span className="block text-sm font-bold text-ka-text-primary">
                Course challenge
              </span>
              <span className="block text-xs text-ka-text-secondary mt-0.5 line-clamp-1">
                Test your knowledge of the skills in this course.
              </span>
            </div>
          </button>
        </nav>
      </aside>
    </>
  );
};
